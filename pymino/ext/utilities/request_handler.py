from .generate import *

class RequestHandler:
    """A class that handles all requests"""
    def __init__(self, bot, session: HTTPClient, proxy: Optional[str] = None):
        self.bot            = bot
        self.pinged:        bool = False
        self.gg:            int = 0
        self.xyz:           str = None
        self.sid:           Optional[str] = None
        self.userId:        Optional[str] = None
        self.session:       HTTPClient = session
        self.base_headers:  dict = {"USER-AGENT": "Dalvik/2.1.0 (Linux; U; Android 7.0; SM-G930V Build/NRD90M; com.narvii.amino.master/3.5.34803)"}
        self.proxy:         dict = {"http": proxy,"https": proxy} if proxy is not None else None

    @ggl
    def service_url(self, url: str) -> str:
        return f"https://service.aminoapps.com/api/v1{url}"
    
    @headers
    def service_headers(self) -> dict:
        return {
            "NDCLANG": "en",
            "ACCEPT-LANGUAGE": "en-US",
            "USER-AGENT": "Dalvik/2.1.0 (Linux; U; Android 7.0; SM-G930V Build/NRD90M; com.narvii.amino.master/3.5.34803)",
            "HOST": "service.aminoapps.com",
            "CONNECTION": "Keep-Alive",
            "ACCEPT-ENCODING": "gzip, deflate, br",
            "NDCAUTH": f"sid={self.sid}",
            "AUID": self.userId,
            }

    def fetch_request(self, method: str) -> Callable:
        request_methods = {
            "GET": self.session.get,
            "POST": self.session.post,
            "DELETE": self.session.delete,
            }
        return request_methods[method]

    @request
    def handler(
        self,
        method: str,
        url: str,
        data: Union[dict, bytes, None] = None,
        content_type: Optional[str] = None
    ) -> dict:
        if not self.pinged:
            self.ping_server()

        url, headers, data = self.service_handler(url, data, content_type)
        if all([method=="POST", data is None]):
            headers["CONTENT-TYPE"] = "application/octet-stream"

        try:
            response: HTTPResponse = self.fetch_request(method)(
                url, data=data, headers=headers, proxies=self.proxy
            )
        except (
            ConnectionError,
            ReadTimeout,
            SSLError,
            ProxyError,
            ConnectTimeout,
        ):
            self.handler(method, url, data, content_type)

        self.print_response(response)
        return self.handle_response(response)

    def service_handler(
        self,
        url: str,
        data: Union[dict, bytes, None] = None,
        content_type: Optional[str] = None
    ) -> Tuple[str, dict, Union[dict, bytes, None]]:

        service_url = self.service_url(url)
        
        headers = {"NDCDEVICEID": device_id()}
        header_mapping = {
            True: self.base_headers,
            False: self.service_headers(),
        }
        headers.update(header_mapping[url.endswith("/g/s/auth/login")])

        if data or content_type:
            headers, data = self.fetch_signature(url, data, headers, content_type)

        return service_url, headers, data

    def fetch_signature(
        self,
        url: str,
        data: str,
        headers: dict,
        content_type: str = None
    ) -> Tuple[dict, Union[dict, bytes, None]]:
        data = data if isinstance(data, bytes) else dumps(data)
        headers.update({
            "CONTENT-LENGTH": f"{len(data)}",
            "CONTENT-TYPE": content_type or "application/json; charset=utf-8",
            "NDC-MSG-SIG": (
                generate_signature(data)
                if url.endswith("/g/s/auth/login")
                else self.run_abc(data)
            ),
        })
        return headers, data

    def handle_response(self, response: HTTPResponse) -> dict:
        if response.status_code != 200:
            with suppress(Exception):
                _response: dict = loads(response.text)
                # TODO: Handle exceptions.
                if _response.get("api:statuscode") == 105:
                    return self.bot.run(self.email, self.password)

            raise Exception(response.text)
            
        return loads(response.text)

    @response
    def signature(self, data: str) -> HTTPResponse:
        return self.session.get(
            url=f"https://gg.o5hej45uqb.repl.co/signature?data={data}",
            headers=self.base_headers
            )

    def parse_signature(self, data: str) -> dict:
        while True:
            try:
                response = self.signature(data)
                if response.status_code == 200:
                    return loads(response.text)["signature"]
                # else:
                #     self.print_status("Failed to generate signature from server, retrying...")
            except Exception:
                self.print_status("Failed to generate signature from server.", "error")
                break

    def ping_server(self) -> HTTPResponse:
        try:
            self.signature(data="ping")
            self.pinged = True
            self.print_status("Pinged server.", "success")
        except Exception as e:
            raise Exception(self.print_status("Failed to ping server, server is most likely down.", "error")) from e

    def run_xyz(self, data: str) -> str:
        data_map = {
            dict: lambda x: dumps(x),
            str: lambda x: x,
            bytes: lambda x: x
            }
        data = data_map[type(data)](data)
        self.gg, self.xyz = [0, self.parse_signature(data)]
        return self.xyz

    def run_abc(self, data: str) -> dict:
        data_map = {
            str: lambda x: loads(x),
            dict: lambda x: x,
            bytes: lambda x: x
            }
        parsed_data = data_map[type(data)](data)

        if isinstance(parsed_data, bytes):
            return self.xyz

        if parsed_data.get("mediaUploadValue") or all([self.abc(parsed_data), self.run_gg()]):
            return self.xyz
        return self.run_xyz(parsed_data)

    def abc(self, data: dict) -> bool:
        return all([self.sid, data.get("clientRefId")])

    def run_gg(self) -> bool: return self.gg < 10

    def print_response(self, response: HTTPResponse) -> None:
        if self.bot.debug:
            print(f"{Fore.BLUE}{Style.BRIGHT}{response.request.method}:{Style.RESET_ALL} {response.url}")

    def print_status(self, message: str, status: str = "warning") -> None:
        if status == "warning":
            print(f"{Fore.YELLOW}{Style.BRIGHT}WARNING:{Style.RESET_ALL} {message}")
        elif status == "success":
            print(f"{Fore.GREEN}{Style.BRIGHT}SUCCESS:{Style.RESET_ALL} {message}")
        elif status == "error":
            print(f"{Fore.RED}{Style.BRIGHT}ERROR:{Style.RESET_ALL} {message}")

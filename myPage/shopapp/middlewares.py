import time
from typing import Any
from django.http import HttpRequest


class ThrottlingMiddleware:

    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.ips = {}

    def __call__(self, request: HttpRequest) -> Any:
        ip = request.META.get('REMOTE_ADDR')
        dt = time.time()
        if self.ips.get(ip, None) is not None:
            if dt - self.ips[ip] < 0.5 and request.method == "POST":
                raise Exception("TO MANY REQUEST")
        self.ips[ip] = dt
        response = self.get_response(request)
        return response

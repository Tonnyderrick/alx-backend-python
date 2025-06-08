from datetime import datetime, time
import logging
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Set up the logger
        self.logger = logging.getLogger('request_logger')
        handler = logging.FileHandler('requests.log')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        start_block = time(21, 0)  # 9 PM
        end_block = time(6, 0)     # 6 AM

        # Restrict access between 9 PM and 6 AM
        if now >= start_block or now <= end_block:
            return HttpResponseForbidden("Access to chat is restricted between 9 PM and 6 AM")

        response = self.get_response(request)
        return response

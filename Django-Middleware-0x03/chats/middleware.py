import time
from django.http import HttpResponseForbidden

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Stores IP -> list of timestamps (of POST requests/messages)
        self.ip_message_times = {}

        # Limits
        self.MAX_MESSAGES = 5
        self.TIME_WINDOW = 60  # seconds

    def __call__(self, request):
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = time.time()
            message_times = self.ip_message_times.get(ip, [])

            # Keep only timestamps within the TIME_WINDOW (last 60 seconds)
            message_times = [t for t in message_times if now - t < self.TIME_WINDOW]

            if len(message_times) >= self.MAX_MESSAGES:
                return HttpResponseForbidden("Message rate limit exceeded. Please wait before sending more messages.")

            # Add current timestamp and update dict
            message_times.append(now)
            self.ip_message_times[ip] = message_times

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Get client IP address from request headers or remote addr."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # First IP in list is the client IP
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            allowed_roles = ['admin', 'moderator']
            user_role = getattr(user, 'role', None)
            if user_role not in allowed_roles:
                return HttpResponseForbidden("Access denied: insufficient permissions.")
        else:
            return HttpResponseForbidden("Access denied: please login.")

        return self.get_response(request)

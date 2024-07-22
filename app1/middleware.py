# myapp/middleware.py

import threading

class ActionStatusMiddleware:
    _action_performed = False
    _lock = threading.Lock()

    @classmethod
    def perform_action(cls):
        with cls._lock:
            if not cls._action_performed:
                cls._action_performed = True
                return True
        return False

    @classmethod
    def reset_action_status(cls):
        with cls._lock:
            cls._action_performed = False

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        if request.path == '/action-status/':
            self.reset_action_status()
        return response

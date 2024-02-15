import traceback
import logging
from django.urls import reverse
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


class ExceptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        
        traceback_info = traceback.format_exc()
        logger.error(f"request_path: {request.path}, traceback_info: {traceback_info}")
        return redirect(reverse("rainAU:error"))

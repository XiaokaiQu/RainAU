import traceback
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


class ExceptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):

        traceback_info = traceback.format_exc()
        logger.info(f"request_path: {request.path}, traceback_info: {traceback_info}")
        return JsonResponse({"code": -1, "msg": "error"}, status=500)

import logging

from rest_framework import status

logger = logging.getLogger(__name__)


class ResponseWrapper:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        return self.process_response(request, response)

    def _process_error_messages(self, error_messages):
        all_messages = []
        for value in error_messages.values():
            if isinstance(value, list):
                all_messages.extend(value)
            else:
                all_messages.append(value)
        return all_messages

    def process_response(self, request, response):

        status_code = response.status_code
        content_type = response.get('Content-Type', None)
        if content_type is None or content_type != 'application/json':
            return response

        try:
            data = response.data
        except AttributeError:
            data = None

        is_success = status.is_success(status_code)
        is_error = status.is_client_error(status_code) or status.is_server_error(status_code)

        response.data = {
            'success': is_success,
        }

        if is_error:
            collected_errors = data
            data = None
            response.data['error_messages'] = self._process_error_messages(collected_errors)
        else:
            response.data['data'] = data

        response._is_rendered = False
        try:
            response.render()
        except AttributeError as e:
            logger.error("Can't wrap and render response: {}. Status code was {}".format(e, response.status_code))

        return response

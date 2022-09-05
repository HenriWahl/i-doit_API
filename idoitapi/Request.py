"""
Base class for JSON RPC API requests
"""

from idoitapi.API import API
from idoitapi.APIException import JSONRPC


class Request(object):

    def __init__(self, api=None, api_params=None):
        """
        :param api: (optional) a :py:mod:`~idoitapi.API` object
        :param api_params: (optional) parameters to pass to the API
        """
        if api is None:
            if api_params is None:
                api_params = {}
            api = API(**api_params)
        self._api = api

    @staticmethod
    def require_success_for(result):
        """
        Check for success and return identifier

        :param dict result: Response from API request
        :return: Identifier
        :rtype: int
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        if 'id' not in result or not isinstance(result['id'], int) or \
                'success' not in result or not result['success']:
            message = 'Bad result'
            if 'message' in result:
                message += ': ' + result['message']
            raise JSONRPC(message=message)

        return result['id']

    @staticmethod
    def require_success_without_identifier(result):
        """
        Check for success but ignore identifier

        :param dict result: Result
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        if 'success' not in result or not result['success']:
            message = 'Bad result'
            if 'message' in result:
                message += ': ' + result['message']
            raise JSONRPC(message=message)

    @staticmethod
    def require_success_for_all(results):
        """
        Check whether each request in a batch was successful

        :param results: Results
        :type results: list(dict)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        for result in results:
            Request.require_success_without_identifier(result)
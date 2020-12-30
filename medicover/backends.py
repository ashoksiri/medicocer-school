
from oauth2_provider.oauth2_backends import JSONOAuthLibCore
import json

class KeerthanaOauthLib(JSONOAuthLibCore):
    """
        Extends the default OAuthLibCore to parse correctly application/json requests
        """

    def extract_body(self, request):


        """
        Extracts the JSON body from the Django request object
        :param request: The current django.http.HttpRequest object
        :return: provided POST parameters "urlencodable"
        """


        try:
            if request.content_type != 'application/json':
                data = request.POST.dict().items()
                return data

            body = json.loads(request.body.decode("utf-8")).items()
        except ValueError:
            body = ""

        return body

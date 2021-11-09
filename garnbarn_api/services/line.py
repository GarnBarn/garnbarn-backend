import requests
import json


class LineApiError(Exception):
    def __init__(self, line_error_object):
        self.line_error_object = {
            "line_error": line_error_object
        }

    def __str__(self):
        return json.dumps(self.__line_error_object)


class LineLoginPlatformHelper:
    GET_ACCESS_TOKEN_API = "https://api.line.me/oauth2/v2.1/token"
    GET_USER_PROFILE_API = "https://api.line.me/v2/profile"

    def __init__(self, user_access_token=None, credential_file="line-config.json"):
        """The Line Login API wrapper

        Args:
            user_access_token (string, optional): The user's access token for LINE Login API. Defaults to None.
            credential_file (str, optional): 
                The credential file containing the credential for LINE Login Channel. Defaults to "line-config.json".
        """
        # Automatic load credential from file
        credential_file_io = open(credential_file)
        credential = json.load(credential_file_io)
        self.__channel_secret = credential["login"]["channel_secret"]
        self.__channel_id = credential["login"]["channel_id"]
        self.__user_access_token = user_access_token

    def verify_login_code(self, code, redirect_uri, client_id):
        """Verify the code from LINE Login and return the Access Token

        Args:
            code (string): The code from LINE Login (From frontend)
            redirect_uri (string): The redirect uri after user logged in from line
            client_id (string): The client id that user signed into.

        Raises:
            AssertionError: When the client id and the channel id is not the same
            LineApiError: If LINE API not response 200 status_code 
        """
        if client_id != self.__channel_id:
            raise AssertionError(
                "Client id is diffriend from the client id in the server.")
        body = {
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": self.__channel_secret,
            "grant_type": "authorization_code"
        }
        response = requests.post(self.GET_ACCESS_TOKEN_API, body)
        if response.status_code != 200:
            raise LineApiError(response.json())
        self.__user_access_token = response.json()["access_token"]

    def get_user_profile(self):
        """Get the LINE user profile

        Raises:
            TypeError: If the user_access_token is not set or type of user_access_token is not string
            LineApiError: If LINE API not response 200 status_code 

        Returns:
            Dict: The LINE User profile object
                    https://developers.line.biz/en/reference/line-login-v2/#get-profile-response
        """
        if type(self.__user_access_token) != str:
            raise TypeError(
                "The user access token must be a string (Make sure that you set it correctly while init this object or call verify_login_code")
        headers = {
            "Authorization": f"Bearer {self.__user_access_token}"
        }
        response = requests.get(self.GET_USER_PROFILE_API, headers=headers)
        if response.status_code != 200:
            raise LineApiError(response.json())
        return response.json()

"""This File contain the custom authentication for checking the ID Token from Firebase Auth.
"""
from rest_framework import authentication, exceptions
from django.http import HttpRequest
from firebase_admin import credentials, auth, initialize_app
from .models import CustomUser
import os

if os.path.exists('firebase-adminsdk-credential.json'):
    # If file exists, Load the credential file.
    credential = credentials.Certificate(
        'firebase-adminsdk-credential.json')
else:
    # Set credential to None to initilize_app with DEFAULT firebase credential
    credential = None
# Initilize Firebase App.
initialize_app(credential)


class FirebaseAuthIDTokenAuthentication(authentication.TokenAuthentication):
    keyword = "Bearer"
    model = None

    def authenticate_credentials(self, key):
        try:
            decoded_token = auth.verify_id_token(key)
        except auth.InvalidIdTokenError:
            raise exceptions.AuthenticationFailed(
                "The Credential provided in the request is invalid. The ID Token must be generated from Firebase Auth.", code=401)
        except auth.ExpiredIdTokenError:
            raise exceptions.AuthenticationFailed(
                "The Credential provided in the request is expired", code=401)
        if not decoded_token.get("uid"):
            raise exceptions.AuthenticationFailed(
                "Invalid credential", code=401)
        try:
            user_model = CustomUser.objects.get(uid=decoded_token.get("uid"))
        except CustomUser.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                "No user with this uid in the recoard. Please call create user api first.", code=403)

        return (user_model, None)

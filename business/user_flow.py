from apis.user_api import UserAPI


class UserFlow:
    def __init__(self, api_client):
        self.user_api = UserAPI(api_client)

    def register_user(self, username, email, password):
        return self.user_api.user_register(username, email, password)

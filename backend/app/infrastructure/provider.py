from app.core.settings import Settings
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed


users = Settings.users


class UsernameAndPasswordProvider(AuthProvider):
    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        if len(username) < 3:
            """Form data validation"""
            raise FormValidationError(
                {"username": "Имя пользователя длинне чем 3 символа."}
            )
        if username in users and password == Settings.admin_panel_password:
            request.session.update({"username": username})
            return response
        raise LoginFailed("Неправильные логин или пароль.")

    async def is_authenticated(self, request) -> bool:
        if request.session.get("username", None) in users:
            request.state.user = users.get(request.session["username"])
            return True
        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        user = request.state.user
        custom_app_title = "Привет " + user["name"] + "!"
        custom_logo_url = None
        if user.get("company_logo_url", None):
            custom_logo_url = request.url_for(
                "static", path=user["company_logo_url"]
            )
        return AdminConfig(
            app_title=custom_app_title,
            logo_url=custom_logo_url,
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user
        photo_url = None
        if user.get("avatar") is not None:
            photo_url = request.url_for("static", path=user["avatar"])
        return AdminUser(username=user["name"], photo_url=photo_url)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response

from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

from app.config import get_settings

class SettingsAuthProvider(AuthProvider):
    """Custom Authentication Provider for Starlette Admin"""

    def __init__(self) -> None:
        super().__init__(login_path="/login", logout_path="/logout") # type: ignore
        self.settings = get_settings()

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response
    ) -> Response:
        if not username or not password:
            raise FormValidationError({"Login": "Username and password are required."})
        
        if (
            username == self.settings.admin_username 
            and password == self.settings.admin_password
        ):
            request.session["admin_user"] = username
            return response
        
        raise LoginFailed("Invalid admin username or password.")
    
    async def is_authenticated(self, request: Request) -> bool:
        return bool(request.session.get("admin_user"))
    
    def get_admin_user(self, request: Request) -> AdminUser | None:
        username = request.session.get("admin_user")
        if username:
            return AdminUser(username=username)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
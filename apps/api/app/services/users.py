from app.auth.passwords import PasswordService
from app.models.user import User
from app.repositories.users import UserRepository, normalise_email
from app.schemas.users import UserRegistration


class EmailAlreadyRegisteredError(ValueError):
    pass


class RegistrationService:
    def __init__(
        self,
        repository: UserRepository,
        passwords: PasswordService,
    ) -> None:
        self._repository = repository
        self._passwords = passwords

    async def register(self, request: UserRegistration) -> User:
        email = normalise_email(str(request.email))

        if await self._repository.find_by_email(email):
            raise EmailAlreadyRegisteredError

        user = User(
            email=email,
            password_hash=self._passwords.hash(request.password),
            display_name=request.display_name.strip(),
            timezone="Australia/Sydney",
        )
        return await self._repository.add(user)

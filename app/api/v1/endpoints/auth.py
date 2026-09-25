from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.users import UserCreateSchema, UserReadSchema
from app.services.users import UsersService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post(
    "/register", 
    response_model=UserReadSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя"
)
async def register_user(
    user_data: UserCreateSchema,
    auth_service: UsersService = Depends(get_current_user),
):
    try:
        user = await auth_service.register_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )


@router.post(
    "/login", 
    summary="Вход в систему (получение JWT токена в HttpOnly Cookie)"
)
async def login_user(
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends(),
    auth_service: UsersService = Depends(get_current_user),
):
    try:
        # FastAPI OAuth2Form использует .username (тут передаём email)
        access_token = await auth_service.authenticate_user(
            email=credentials.username, 
            password=credentials.password
        )
        
        # Безопасно кладём JWT токен в куки
        response.set_cookie(
            key="booking_access_token", 
            value=access_token, 
            httponly=True
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=str(e)
        )


@router.post(
    "/logout", 
    summary="Выход из системы (удаление JWT из Cookie)"
)
async def logout_user(response: Response):
    response.delete_cookie(key="booking_access_token")
    return {"message": "Успешный выход из системы"}
import logging

from fastapi import APIRouter, Form, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse

from src.api.auth.dependencies import get_auth_service, oauth2_scheme
from src.api.auth.v1.response.auth_token_response import AuthTokenResponse
from src.domain.auth.model.auth_credentials import AuthCredentials
from src.domain.auth.service.auth_service import AuthService

logger = logging.Logger(__name__)

router = APIRouter(
    prefix="/auth/v1",
    tags=["Auth"],
    dependencies=[Depends(get_auth_service)]
)


@router.post(path="/signup", status_code=status.HTTP_201_CREATED)
async def signup(full_name: str = Form(), email: str = Form(),
                 password: str = Form(), auth_service: AuthService = Depends(get_auth_service)):
    await auth_service.register_new_user(full_name=full_name, email=email, password=password)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User created!"})


@router.post(path="/signin", status_code=status.HTTP_200_OK)
async def signin(form_data: OAuth2PasswordRequestForm = Depends(),
                 auth_service: AuthService = Depends(get_auth_service)):
    auth_credentials = AuthCredentials(email=form_data.username, password=form_data.password)
    auth_token = await auth_service.authorize_login(auth_credentials=auth_credentials)
    response = AuthTokenResponse.from_domain(auth_token)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response.model_dump(exclude_none=True)
    )


@router.delete(path="/signout", status_code=status.HTTP_204_NO_CONTENT)
async def signout(access_token: str = Depends(oauth2_scheme), auth_service: AuthService = Depends(get_auth_service)):
    await auth_service.signout(access_token=access_token)
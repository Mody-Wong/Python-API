from functools import lru_cache

import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from core.config import get_settings

bearer_scheme = HTTPBearer(auto_error=False)


class Auth0Error(Exception):
    pass


@lru_cache
def get_jwks() -> dict:
    settings = get_settings()
    jwks_url = f"https://{settings.auth0_domain}/.well-known/jwks.json"

    response = requests.get(jwks_url, timeout=5)
    response.raise_for_status()

    return response.json()


def get_signing_key(token: str) -> dict:
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError as exc:
        raise Auth0Error("Invalid token header") from exc

    jwks = get_jwks()

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            return key

    raise Auth0Error("Unable to find matching signing key")


def require_auth(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization token",
        )

    settings = get_settings()
    token = credentials.credentials

    try:
        signing_key = get_signing_key(token)

        payload = jwt.decode(
            token,
            signing_key,
            algorithms=[settings.auth0_algorithms],
            audience=settings.auth0_audience,
            issuer=settings.auth0_authority,
        )

        return payload

    except (JWTError, Auth0Error, requests.RequestException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token",
        )
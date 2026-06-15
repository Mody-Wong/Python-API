from fastapi import APIRouter, Depends

from core.auth import require_auth

router = APIRouter(prefix="/me", tags=["auth"])


@router.get("")
def get_me(user: dict = Depends(require_auth)) -> dict:
    return {
        "sub": user.get("sub"),
        "email": user.get("email"),
        "permissions": user.get("permissions", []),
    }

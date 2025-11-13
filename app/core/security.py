from datetime import datetime, timedelta
from typing import Optional, Union

from jose import JWTError, jwt

from app.core.config import settings
from app.utils.hashing import get_password_hash, verify_password

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, int],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Crea un JWT de acceso usando SECRET_KEY y HS256.
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta

    to_encode = {
        "sub": str(subject),
        "exp": expire,
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[str]:
    """
    Decodifica el token y devuelve el 'sub' (user_id) si es válido.
    Si falla, devuelve None.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        subject: str = payload.get("sub")
        return subject
    except JWTError:
        return None


# Reexportar funciones de hashing para compatibilidad
__all__ = [
    "create_access_token",
    "decode_access_token",
    "get_password_hash",
    "verify_password",
]

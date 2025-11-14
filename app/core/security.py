from datetime import datetime, timedelta
from typing import Optional, Union, Dict, Any

from fastapi.security import OAuth2PasswordBearer   # 👈 NUEVO
from jose import JWTError, jwt

from app.core.config import settings
from app.utils.hashing import get_password_hash, verify_password

ALGORITHM = "HS256"

# 👇 NUEVO: esquema OAuth2 para obtener el token desde el header Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"  # /api/v1/auth/login
)


def create_access_token(
    subject: Union[str, int],
    expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta

    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


# 🔧 CAMBIADO: ahora devuelve el payload completo (dict), no solo el sub
def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodifica el token y devuelve el payload (dict) si es válido.
    Si falla, devuelve None.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload
    except JWTError:
        return None


# Reexportar funciones para usarlas desde app.core.security
__all__ = [
    "oauth2_scheme",      # 👈 NUEVO
    "create_access_token",
    "decode_access_token",  # 👈 nombre corregido
    "get_password_hash",
    "verify_password",
]

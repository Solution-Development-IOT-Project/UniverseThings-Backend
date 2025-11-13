from passlib.context import CryptContext

# BCRYPT → estándar para FastAPI + seguridad fuerte
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Genera un hash seguro usando bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si el password ingresado coincide con el hash almacenado.
    """
    return pwd_context.verify(plain_password, hashed_password)

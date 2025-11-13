from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.models.role import Role


def init_db(db: Session) -> None:

    default_roles = ["admin", "farmer", "viewer"]

    for role_name in default_roles:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            new_role = Role(name=role_name)
            db.add(new_role)

    db.commit()
    admin_email = "admin@agrodrone.com"
    admin_user = db.query(User).filter(User.email == admin_email).first()

    if not admin_user:
        password_hashed = get_password_hash("admin123")

        admin_role = db.query(Role).filter(Role.name == "admin").first()

        new_admin = User(
            email=admin_email,
            full_name="Administrador AgroDrone",
            hashed_password=password_hashed,
            role_id=admin_role.id if admin_role else None,
            is_active=True,
        )

        db.add(new_admin)
        db.commit()

    print("Base de datos inicializada correctamente.")

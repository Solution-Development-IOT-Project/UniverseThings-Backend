from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field
from pydantic import ConfigDict
from sqlalchemy.orm import Query

T = TypeVar("T")


class PaginationParams(BaseModel):
    """
    Parámetros estándar para paginación vía query params.
    Ejemplo en endpoint:
    - ?limit=20&offset=40
    """
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Respuesta estándar paginada.
    """
    items: List[T]
    total: int
    limit: int
    offset: int

    model_config = ConfigDict(from_attributes=True)


def paginate(
    query: Query,
    params: Optional[PaginationParams] = None,
) -> (List, int):
    """
    Aplica paginación a un SQLAlchemy Query.

    Retorna:
    - items: lista de filas de la página actual
    - total: número total de filas sin paginación

    Uso típico:
        params = PaginationParams(limit=10, offset=0)
        items, total = paginate(db.query(User), params)
    """
    if params is None:
        params = PaginationParams()

    total = query.order_by(None).count()  # eliminar ORDER BY para el count

    items = (
        query
        .limit(params.limit)
        .offset(params.offset)
        .all()
    )

    return items, total

"""
AttributesRepository — CRUD puro para SessionAttributes.

Contrato: NÃO aplica clamp (clamp é da engine). NÃO valida ranges.
NÃO aplica consequência. Apenas persiste o estado já calculado.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from models.session_attributes import SessionAttributes

_VALID_ATTRS = (
    "energia",
    "reputacao",
    "networking",
    "ansiedade",
    "produtividade",
    "aprendizado",
)


def get(db: Session, session_id: int) -> SessionAttributes | None:
    return db.get(SessionAttributes, session_id)


def update(
    db: Session,
    session_id: int,
    attrs: dict[str, int],
) -> SessionAttributes | None:
    """Atualiza atributos da sessão a partir de um dict.

    Aceita dict parcial — só toca o que está presente. Atributos
    desconhecidos são silenciosamente ignorados (não é responsabilidade
    do repositório validar — a engine entrega valores consistentes).
    """
    row = db.get(SessionAttributes, session_id)
    if row is None:
        return None
    for key in _VALID_ATTRS:
        if key in attrs:
            setattr(row, key, attrs[key])
    db.commit()
    db.refresh(row)
    return row

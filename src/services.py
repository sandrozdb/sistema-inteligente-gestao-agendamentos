"""Validações e regras de negócio independentes da interface e do banco."""

from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation

STATUS_VALIDOS = {"agendado", "concluido", "cancelado"}


def texto_obrigatorio(valor: str, campo: str) -> str:
    texto = (valor or "").strip()
    if not texto:
        raise ValueError(f"{campo} é obrigatório.")
    return texto


def validar_email(email: str) -> str:
    email = (email or "").strip()
    if email and ("@" not in email or "." not in email.split("@")[-1]):
        raise ValueError("E-mail inválido.")
    return email


def validar_preco(valor: str) -> Decimal:
    try:
        preco = Decimal(str(valor).replace(",", "."))
    except (InvalidOperation, ValueError):
        raise ValueError("Preço inválido.") from None
    if preco <= 0:
        raise ValueError("O preço deve ser maior que zero.")
    return preco.quantize(Decimal("0.01"))


def validar_data_hora(valor: str) -> datetime:
    try:
        inicio = datetime.strptime(valor.strip(), "%d/%m/%Y %H:%M")
    except (ValueError, AttributeError):
        raise ValueError("Use o formato DD/MM/AAAA HH:MM.") from None
    return inicio


def validar_status(status: str) -> str:
    status = (status or "").strip().lower()
    if status not in STATUS_VALIDOS:
        raise ValueError("Status inválido.")
    return status


def horarios_conflitam(inicio_a: datetime, duracao_a: int, inicio_b: datetime, duracao_b: int) -> bool:
    fim_a = inicio_a + timedelta(minutes=duracao_a)
    fim_b = inicio_b + timedelta(minutes=duracao_b)
    return inicio_a < fim_b and inicio_b < fim_a

"""Acesso ao MySQL com consultas parametrizadas."""

import os
from contextlib import contextmanager

from dotenv import load_dotenv
import mysql.connector

load_dotenv()


@contextmanager
def conexao():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "gestao_agendamentos"),
    )
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def listar_agendamentos():
    sql = """
        SELECT a.id, c.nome AS cliente, p.nome AS profissional,
               s.nome AS servico, a.inicio, a.status
          FROM agendamentos a
          JOIN clientes c ON c.id = a.cliente_id
          JOIN profissionais p ON p.id = a.profissional_id
          JOIN servicos s ON s.id = a.servico_id
         ORDER BY a.inicio
    """
    with conexao() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()


def cadastrar_cliente(nome, telefone, email):
    with conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clientes (nome, telefone, email) VALUES (%s, %s, %s)",
            (nome, telefone, email or None),
        )


def cadastrar_profissional(nome, especialidade):
    with conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO profissionais (nome, especialidade) VALUES (%s, %s)",
            (nome, especialidade or None),
        )


def cadastrar_servico(nome, preco, duracao_minutos):
    with conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO servicos (nome, preco, duracao_minutos) VALUES (%s, %s, %s)",
            (nome, preco, duracao_minutos),
        )


def listar_opcoes(tabela):
    permitidas = {"clientes", "profissionais", "servicos"}
    if tabela not in permitidas:
        raise ValueError("Tabela não permitida.")
    with conexao() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {tabela} ORDER BY nome")
        return cursor.fetchall()


def cadastrar_agendamento(cliente_id, profissional_id, servico_id, inicio):
    with conexao() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT duracao_minutos FROM servicos WHERE id = %s", (servico_id,))
        servico = cursor.fetchone()
        if not servico:
            raise ValueError("Serviço não encontrado.")
        cursor.execute(
            """
            SELECT a.inicio, s.duracao_minutos
              FROM agendamentos a
              JOIN servicos s ON s.id = a.servico_id
             WHERE a.profissional_id = %s AND a.status = 'agendado'
               AND a.inicio < DATE_ADD(%s, INTERVAL %s MINUTE)
               AND DATE_ADD(a.inicio, INTERVAL s.duracao_minutos MINUTE) > %s
            """,
            (profissional_id, inicio, servico["duracao_minutos"], inicio),
        )
        if cursor.fetchone():
            raise ValueError("O profissional já possui atendimento nesse intervalo.")
        cursor.execute(
            """INSERT INTO agendamentos
               (cliente_id, profissional_id, servico_id, inicio)
               VALUES (%s, %s, %s, %s)""",
            (cliente_id, profissional_id, servico_id, inicio),
        )


def cancelar_agendamento(agendamento_id):
    with conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE agendamentos SET status = 'cancelado' WHERE id = %s",
            (agendamento_id,),
        )

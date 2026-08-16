# Banco de dados

O modelo possui quatro entidades centrais: clientes, profissionais, serviços e agendamentos.

As chaves estrangeiras preservam os relacionamentos e os índices apoiam consultas por profissional, horário e status. O cancelamento é lógico para manter o histórico.

O esquema não inclui usuários ou autenticação porque essas funcionalidades não fazem parte da reconstrução atual.

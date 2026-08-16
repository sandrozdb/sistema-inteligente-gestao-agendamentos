# Regras de negócio

## Regras implementadas

- nome e telefone do cliente são obrigatórios;
- e-mail, quando preenchido, deve possuir formato básico válido;
- preço e duração de serviços devem ser positivos;
- o status pertence a `agendado`, `concluido` ou `cancelado`;
- agendamentos cancelados permanecem no histórico;
- intervalos sobrepostos são detectados pela função `horarios_conflitam`.

## Regra de conflito

Dois intervalos conflitam quando o início de cada um ocorre antes do término do outro. Horários consecutivos, em que um atendimento começa exatamente quando o anterior termina, são permitidos.

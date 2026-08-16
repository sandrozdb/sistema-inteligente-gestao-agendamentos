# Arquitetura

A reconstrução adota separação entre interface, regras de negócio e acesso aos dados.

No projeto original, Python e MySQL sustentavam o sistema, o Figma era utilizado na prototipação das telas e o Visual Studio apoiava o desenvolvimento. A reconstrução atual mantém Python e MySQL e utiliza Tkinter para disponibilizar uma versão desktop reproduzível.

- `app.py`: janelas, campos, tabela e interação com o usuário;
- `services.py`: validações que podem ser testadas sem interface ou banco;
- `database.py`: conexão, transações e consultas parametrizadas;
- `schema.sql`: tabelas, relacionamentos, restrições e índices.

Essa organização reduz o acoplamento e facilita testes e futuras evoluções para uma API ou aplicação web.

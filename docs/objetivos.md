# Objetivos

## Objetivos funcionais

O que o sistema precisa fazer.

**Tabela 3 — Objetivos funcionais**

| ID | Objetivo |
| -- | -------- |
| OF01 | Permitir cadastro e autenticação de usuários |
| OF02 | Permitir ao autor criar, editar e excluir seus próprios textos |
| OF03 | Controlar o ciclo de publicação, distinguindo rascunho de publicado |
| OF04 | Disponibilizar leitura pública, sem exigir cadastro |
| OF05 | Organizar o conteúdo por categorias e tags |
| OF06 | Permitir busca de textos por termo |
| OF07 | Permitir que usuários autenticados comentem |
| OF08 | Prover moderação de comentários e gestão de usuários |
| OF09 | Manter perfil público do autor |

## Objetivos não-funcionais

Como o sistema precisa se comportar.

**Tabela 4 — Objetivos não-funcionais**

| ID | Categoria | Objetivo |
| -- | --------- | -------- |
| ONF01 | Usabilidade | Interface responsiva, utilizável em telas a partir de 360 pixels de largura |
| ONF02 | Desempenho | A listagem de textos responde em até 2 segundos com base de até 500 registros |
| ONF03 | Segurança | Senhas armazenadas com hash PBKDF2, padrão do Django; proteção contra CSRF, XSS e injeção de SQL pelo ORM e pelos templates do framework |
| ONF04 | Autorização | O autor só edita ou exclui conteúdo de sua autoria; a moderação é restrita a usuários com permissão |
| ONF05 | Portabilidade | Executa em Windows, Linux e macOS sobre Python 3; compatível com navegadores atuais |
| ONF06 | Manutenibilidade | Código em conformidade com a PEP 8, separado em aplicações, versionado em Git com histórico de contribuição por integrante |
| ONF07 | Acessibilidade | HTML semântico, formulários rotulados e contraste adequado |
| ONF08 | Localização | Interface em português do Brasil, datas no fuso `America/Sao_Paulo` |

Os objetivos não-funcionais são verificáveis. ONF02 tem número e base de
comparação; ONF01 tem largura mínima. Objetivo que não pode ser conferido não
serve para cobrar nada de ninguém, inclusive da própria equipe.

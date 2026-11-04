# Plano de testes do Ataraxia

Prática Profissional em Análise e Desenvolvimento de Sistemas  
Universidade Presbiteriana Mackenzie

Versão 2.0, revisada na Iteração 2 (tag `v2`). Esta é a versão em texto do plano entregue em PDF; os casos e o resultado da execução são os mesmos.

## 1 Introdução

Este documento é o plano de testes do Ataraxia, plataforma de blog desenvolvida como projeto do componente Prática Profissional em Análise e Desenvolvimento de Sistemas da Universidade Presbiteriana Mackenzie. Esta é a versão revisada na Iteração 2 (tag v2 do repositório).

O plano parte dos onze casos de uso registrados na análise. Cada fluxo principal, alternativo e de exceção vira pelo menos um caso de teste, e cada regra de negócio tem um caso de teste que a exercita. Os casos de uso UC02, UC03, UC05, UC08 e UC10, descritos em detalhe na análise, têm testes derivados fluxo a fluxo; os demais têm testes derivados do comportamento descrito na lista de casos de uso, na arquitetura e no roteiro de testes manuais do repositório.

### 1.1 Identificação do projeto

- **Título:** Ataraxia
- **Repositório de código-fonte:** github.com/ataraxia-ppads/ataraxia-blog
- **Quadro de acompanhamento:** github.com/orgs/ataraxia-ppads/projects/1
- **Publicação prevista:** blog.ataraxia.dev

### 1.2 Integrantes do grupo

- Felipe Amorim
- Gabriel Vieira Ferreira
- Pedro Emmanuel Esteves
- Rafaela Rarume Alves Perpetuo
- Renan Urtado Challó de Oliveira Jordão

### 1.3 Histórico de revisões

| Versão | Iteração | O que mudou |
| --- | --- | --- |
| 1.0 | Iteração 1 (tag v1) | Plano inicial: 74 casos funcionais (51 automatizados e 23 manuais) e 10 não funcionais. |
| 2.0 | Iteração 2 (tag v2), 4 nov. 2026 | Os 23 casos manuais viraram testes automatizados com o cliente de teste do Django, todos mapeados a um teste existente (apêndice A). CT05.10 e CT11.04 tiveram o resultado esperado alinhado ao comportamento real (redirecionamento para a entrada do admin, e não uma página de acesso negado). CTN02 e CTN09 ganharam teste automatizado; o contraste e o uso só com teclado saíram de CTN09 para o novo CTN11. Novo capítulo 6 com o registro da execução. |

## 2 Estratégia de testes

A organização do plano segue, de forma enxuta, os itens que a IEEE 829 e a ISO/IEC/IEEE 29119-3 recomendam para documentação de teste (IEEE, 2008; ISO, 2021).

### 2.1 Itens testados

O objeto de teste são as três aplicações Django do sistema e os onze casos de uso que elas implementam. Os objetivos não funcionais que admitem verificação objetiva também entram, no capítulo 4.

Quem constrói a aplicação escreve os testes automatizados dela. Rafaela conduz o percurso manual no navegador antes de cada entrega e registra o resultado.

Ficam fora do escopo o funcionamento interno do admin do Django, que já é testado pelo próprio framework (testa-se apenas a configuração feita pelo grupo: quem acessa e o que cada ação faz) (Django Software Foundation, 2026), e a infraestrutura de hospedagem.

### 2.2 Níveis e tipos de teste

Os níveis seguem a divisão clássica entre teste de componente, de sistema e de aceitação (Pressman; Maxim, 2016; Sommerville, 2011).

A coluna Tipo das tabelas do capítulo 3 indica como cada caso é executado: Auto para teste automatizado de unidade ou integração, Manual para execução no navegador. Toda regra de autorização é testada como Auto, porque esconder o botão na tela não é prova de nada: o teste envia a requisição direto ao servidor.

Na Iteração 2, os casos que antes eram manuais passaram a Auto. O cliente de teste do Django percorre as mesmas rotas, formulários e redirecionamentos do navegador e confere o HTML devolvido, mas não executa CSS nem JavaScript. Por isso o que só se vê na tela continua manual (CTN01, CTN07 e CTN11), e o percurso de fumaça no navegador da seção 2.8 permanece antes de cada entrega.

| Nível | O que verifica | Como é executado |
| --- | --- | --- |
| Unidade | Métodos de modelo e validação de formulário: geração de slug, publish(), is_visible(), regras de senha | python manage.py test, com django.test.TestCase |
| Integração | View, URL, permissão e banco juntos: códigos 403 e 404, redirecionamentos, o que é gravado e o HTML devolvido | python manage.py test, com o cliente de teste do Django |
| Sistema | O caso de uso inteiro, pelo navegador, como o usuário o percorre | Automatizado pelo cliente de teste; percurso de fumaça manual antes da entrega |
| Aceitação | As funcionalidades combinadas com o professor | Demonstração ao final de cada iteração |

### 2.3 Técnicas de derivação

• Fluxos do caso de uso. Cada fluxo principal, alternativo e de exceção gera ao menos um caso de teste. É o que garante que o plano cobre tudo o que a análise prometeu.

• Partição de equivalência e valor limite. Aplicadas aos campos com regra: senha com 7 e com 8 caracteres, conforme os validadores de senha do Django (Django Software Foundation, 2026), e comentário com 2.000 e com 2.001 caracteres. São as técnicas funcionais descritas por Myers, Sandler e Badgett (2011) e por Delamaro, Maldonado e Jino (2016).

• Testes negativos de autorização. Para cada operação restrita, uma tentativa feita por quem não tem permissão, com o resultado esperado (403, 404 ou redirecionamento para a autenticação).

### 2.4 Ambiente

| Ambiente | Banco | Uso |
| --- | --- | --- |
| Desenvolvimento | SQLite | Testes automatizados, na máquina de cada integrante |
| Verificação contínua | SQLite | Testes, estilo PEP 8 e migrações a cada Pull Request, em Ubuntu com Python 3.14 (GitHub Actions) |
| Publicação | PostgreSQL | Execução manual antes da entrega, em blog.ataraxia.dev (ainda não publicado) |

Os testes manuais são feitos nas versões atuais do Chrome e do Firefox, em tela de computador e em tela de 360 pixels de largura, emulada pelas ferramentas de desenvolvedor do navegador.

### 2.5 Dados de teste

A base de teste é o conteúdo de demonstração do repositório, carregado por fixture: 10 textos, um deles em rascunho, com datas de publicação diferentes entre si, uma palavra incomum no título de um único texto e outra no corpo de um texto diferente. A esses dados somam-se quatro usuários fixos. Os testes automatizados criam os próprios dados em cada teste e não dependem da fixture, para que a ordem de execução não altere o resultado.

| Usuário | Papel | Uso nos testes |
| --- | --- | --- |
| ana | Autora | Dona dos textos da carga, inclusive do rascunho |
| bruno | Autor | Tenta alterar o que é de ana |
| moderador | Moderador | Opera o admin nos casos UC11 e UC13 |
| visitante | Sem sessão | Navega sem estar autenticado |

### 2.6 Critérios

• Entrada. A aplicação a testar está integrada ao main, as migrações aplicam sem erro e a fixture carrega.

• Suspensão. Se a listagem (UC01) ou a autenticação (UC06) falha, a execução manual é suspensa, porque quase todos os outros casos dependem delas.

• Saída. Todos os testes automatizados passam e nenhum caso de teste manual de autorização, de regra de negócio ou de fluxo principal está com resultado Falhou. Falha de fluxo alternativo pode seguir para a entrega se estiver registrada como pendência no quadro.

### 2.7 Registro de defeitos

Cada falha vira uma issue no repositório, com o identificador do caso de teste no título, os passos para reproduzir e o resultado obtido. A issue entra no quadro de acompanhamento atribuída a quem é dono da aplicação. A correção é feita por Pull Request que acrescenta, quando possível, um teste automatizado que reproduz a falha.

### 2.8 Execução

Os testes automatizados rodam a cada Pull Request, antes da revisão, e o revisor confere que passam. O percurso de fumaça no navegador e os testes manuais do capítulo 4 acontecem ao final de cada iteração, antes da entrega, e são registrados com data, versão (a tag do repositório) e quem executou.

## 3 Casos de teste

O identificador tem a forma CTnn.mm, em que nn é o número do caso de uso e mm a sequência dentro dele. A coluna Cenário aponta o fluxo (FP para o principal, A para alternativo, E para exceção) ou a regra de negócio (RN) que o caso exercita. Salvo indicação em contrário, os dados são os da carga de demonstração e os usuários são os da tabela de usuários de teste.

### 3.1 UC01: Listar posts publicados

| ID | Cenário | Passos e dados | Resultado esperado | Tipo |
| --- | --- | --- | --- | --- |
| CT01.01 | FP | Sem sessão, abrir a página inicial | Listagem com os 9 textos publicados, do mais recente para o mais antigo | Auto |
| CT01.02 | RN01 | Sem sessão, procurar o rascunho de ana na listagem | O rascunho não aparece | Auto |
| CT01.03 | Paginação | Com mais textos que o tamanho da página, abrir a segunda página | Os textos restantes aparecem, sem repetir nenhum da primeira | Auto |
| CT01.04 | Base vazia | Sem nenhum texto publicado, abrir a página inicial | Mensagem informando que ainda não há textos | Auto |

### 3.2 UC02: Ler post

| ID | Cenário | Passos e dados | Resultado esperado | Tipo |
| --- | --- | --- | --- | --- |
| CT02.01 | FP | Sem sessão, clicar em um texto da listagem | Exibe título, autor, data de publicação e corpo | Auto |
| CT02.02 | FP, RN02 | Abrir texto com dois comentários aprovados e um reprovado | Os dois aprovados aparecem, do mais antigo para o mais recente; o reprovado não aparece | Auto |
| CT02.03 | A1 | Sem sessão, abrir um texto publicado | No lugar do formulário de comentário, convite para entrar ou cadastrar-se | Auto |
| CT02.04 | A2 | Abrir texto sem comentários | Aviso de que ainda não há comentários | Auto |
| CT02.05 | E1 | Acessar o endereço de um slug que não existe | Página de erro 404 | Auto |
| CT02.06 | E2, RN01 | Sem sessão, e depois como bruno, acessar o endereço do rascunho de ana | Erro 404 nas duas tentativas, e não 403 | Auto |
| CT02.07 | RN01 | Como ana, acessar o endereço do próprio rascunho | O texto é exibido à autora | Auto |

### 3.3 UC03: Buscar post

| ID | Cenário | Passos e dados | Resultado esperado | Tipo |
| --- | --- | --- | --- | --- |
| CT03.01 | FP | Buscar a palavra incomum do título de um único texto | Só aquele texto, com a quantidade encontrada e o termo mantido no campo | Auto |
| CT03.02 | FP, RN03 | Buscar a palavra incomum do corpo de outro texto, que não está em título nenhum | O texto aparece no resultado | Auto |
| CT03.03 | RN03 | Repetir CT03.01 com a palavra toda em maiúsculas | Mesmo resultado de CT03.01 | Auto |
| CT03.04 | FP | Repetir CT03.01 com espaços antes e depois da palavra | Mesmo resultado de CT03.01 | Auto |
| CT03.05 | FP | Com uma busca aplicada, acionar a opção de limpar | A listagem completa volta | Auto |
| CT03.06 | A1 | Enviar a busca sem termo | Listagem completa, como em UC01 | Auto |
| CT03.07 | A2, RN05 | Com mais resultados que uma página, avançar para a segunda | Os resultados restantes, com o termo preservado no endereço | Auto |
| CT03.08 | E1 | Buscar um termo que não existe em nenhum texto | Aviso de nada encontrado e opção de voltar à listagem completa | Auto |
| CT03.09 | E2 | Acessar /?q=termo&page=99 | Erro 404 | Auto |
| CT03.10 | RN04 | Buscar um termo que só existe no rascunho de ana | Nada encontrado, com contagem zero | Auto |
| CT03.11 | RN05 | Abrir direto o endereço /?q= seguido da palavra de CT03.01 | Mesmo resultado de CT03.01 | Auto |

### 3.4 UC05: Cadastrar-se

| ID | Cenário | Passos e dados | Resultado esperado | Tipo |
| --- | --- | --- | --- | --- |
| CT05.01 | FP | Cadastrar carla, e-mail novo e senha Ataraxia#2026 | Conta e perfil criados, sessão iniciada e redirecionamento para a listagem | Auto |
| CT05.02 | E1 | Cadastrar com o nome de usuário ana | Erro indicando o campo nome de usuário; demais campos preservados, senha em branco | Auto |
| CT05.03 | E1 | Cadastrar com o e-mail de ana | Erro indicando o campo e-mail | Auto |
| CT05.04 | E2, RN07 | Senha com 7 caracteres: Atx#202 | Recusa informando o mínimo de 8 caracteres | Auto |
| CT05.05 | RN07 | Senha com exatamente 8 caracteres: Atx#2026 | Senha aceita | Auto |
| CT05.06 | E2, RN07 | Senha 48271935, só numérica | Recusa informando que a senha é inteiramente numérica | Auto |
| CT05.07 | E2, RN07 | Senha password, da lista de senhas comuns | Recusa informando que a senha é muito comum | Auto |
| CT05.08 | E2, RN07 | Usuário carlamendes com senha carlamendes1 | Recusa informando que a senha é parecida com o nome de usuário | Auto |
| CT05.09 | RN06 | Após CT05.01, consultar o campo de senha no banco | O valor começa com pbkdf2_sha256$; a senha digitada não aparece em lugar nenhum | Auto |
| CT05.10 | RN08 | Como carla, acessar /admin/ | Redirecionada para a tela de entrada do admin; nenhum conteúdo do admin é exibido, porque a conta nova tem só o papel de autor | Auto |
| CT05.11 | A1 | Na tela de cadastro, acionar o vínculo para quem já tem conta | Abre a tela de autenticação | Auto |

### 3.5 UC06: Autenticar-se

| ID | Cenário | Passos e dados | Resultado esperado | Tipo |
| --- | --- | --- | --- | --- |
| CT06.01 | FP | Entrar como ana com a senha correta | Acesso liberado, com o nome da autora no topo da página | Auto |
| CT06.02 | Senha errada | Entrar como ana com senha errada | Mensagem de erro que não diz qual campo falhou | Auto |
| CT06.03 | Usuário inexistente | Entrar como zeca, que não existe | A mesma mensagem de CT06.02, para não revelar quem tem conta | Auto |
| CT06.04 | Sair | Autenticada, acionar a saída e depois abrir o editor | Sessão encerrada; o editor redireciona para a autenticação | Auto |
| CT06.05 | Retorno | Sem sessão, abrir o editor, autenticar-se | Depois da autenticação, volta ao editor | Auto |

### 3.6 UC07: Manter perfil

| ID | Cenário | Passos e dados | Resultado esperado | Tipo |
| --- | --- | --- | --- | --- |
| CT07.01 | Editar | Como ana, alterar nome de exibição e biografia e salvar | Alteração gravada e visível no perfil público | Auto |
| CT07.02 | Perfil público | Sem sessão, abrir o perfil de ana | Exibe nome de exibição e biografia | Auto |
| CT07.03 | Autorização | Como bruno, enviar a edição de perfil com dados de ana | Só o perfil de bruno é alterado: a edição sempre atua sobre o usuário da sessão | Auto |
| CT07.04 | Sem sessão | Sem sessão, abrir a edição de perfil | Redireciona para a autenticação | Auto |

### 3.7 UC08: Manter post

| ID | Cenário | Passos e dados | Resultado esperado | Tipo |
| --- | --- | --- | --- | --- |
| CT08.01 | FP, RN12 | Como ana, criar texto com título Primeiro teste e corpo, sem mexer na opção de comentários | Gravado como rascunho com slug primeiro-teste e aberto a comentários; aparece em Meus textos e não na listagem pública | Auto |
| CT08.02 | E1 | Salvar com título vazio | Indica o campo título e preserva o corpo digitado | Auto |
| CT08.03 | E1 | Salvar com corpo vazio | Indica o campo corpo e preserva o título | Auto |
| CT08.04 | A3 | Criar outro texto com o título Primeiro teste | Slug primeiro-teste-2 | Auto |
| CT08.05 | A1 | Como ana, editar o corpo do próprio texto | Alteração gravada, com a data de modificação atualizada | Auto |
| CT08.06 | E2, RN09 | Como bruno, abrir o endereço de edição de um texto de ana | Erro 403 | Auto |
| CT08.07 | E2, RN09 | Como bruno, enviar direto ao servidor a exclusão de um texto de ana | Erro 403, e o texto continua existindo | Auto |
| CT08.08 | A2, RN11 | Como ana, excluir um texto com dois comentários e confirmar | Pede confirmação avisando que é irreversível; texto e comentários excluídos | Auto |
| CT08.09 | A2 | Acionar a exclusão e cancelar na confirmação | Nada é excluído | Auto |
| CT08.10 | RN10 | Publicar um texto, depois alterar o título | O slug continua o mesmo | Auto |
| CT08.11 | Sem sessão | Sem sessão, abrir o editor | Redireciona para a autenticação | Auto |

### 3.8 UC09: Publicar post

| ID | Cenário | Passos e dados | Resultado esperado | Tipo |
| --- | --- | --- | --- | --- |
| CT09.01 | Publicar | Como ana, publicar o próprio rascunho | Passa a aparecer na listagem pública, com a data de publicação registrada | Auto |
| CT09.02 | Despublicar | Despublicar o texto de CT09.01 | Some da listagem pública; o endereço responde 404 ao visitante | Auto |
| CT09.03 | Autorização | Como bruno, enviar direto ao servidor a publicação de um rascunho de ana | Erro 403, e o texto continua em rascunho | Auto |
| CT09.04 | RN10 | Despublicar e publicar de novo o mesmo texto | O endereço do texto não muda | Auto |

### 3.9 UC10: Comentar post

| ID | Cenário | Passos e dados | Resultado esperado | Tipo |
| --- | --- | --- | --- | --- |
| CT10.01 | FP, RN14 | Como bruno, comentar em um texto publicado | Comentário gravado como aprovado e exibido com autor e data | Auto |
| CT10.02 | A1, RN13 | Sem sessão, enviar o comentário direto ao servidor | Redireciona para a autenticação, e nada é gravado | Auto |
| CT10.03 | A2, RN17 | Como bruno, abrir texto de ana com comentários encerrados e enviar um comentário direto ao servidor | Aviso no lugar do formulário; a gravação é recusada | Auto |
| CT10.04 | E1 | Enviar comentário vazio e depois só com espaços | Recusa nas duas tentativas | Auto |
| CT10.05 | E1 | Enviar comentário com 2.000 caracteres e outro com 2.001 | O primeiro é aceito; o segundo é recusado, preservando o texto digitado | Auto |
| CT10.06 | E2 | Abrir o texto, despublicá-lo em outra sessão e então enviar o comentário | Recusa informando que o texto não está mais disponível | Auto |
| CT10.07 | RN15 | Comentar &lt;script&gt;alert(1)&lt;/script&gt; | O texto aparece literalmente na página e nada é executado | Auto |
| CT10.08 | RN16 | Como bruno, enviar o comentário com o campo de autor forjado para ana | O comentário é gravado em nome de bruno | Auto |
| CT10.09 | RN17 | Como ana, desmarcar no editor a opção de aceitar comentários de um texto que já tem comentários | Os comentários existentes continuam visíveis, e o formulário dá lugar ao aviso de comentários encerrados | Auto |

### 3.10 UC11: Moderar comentário

| ID | Cenário | Passos e dados | Resultado esperado | Tipo |
| --- | --- | --- | --- | --- |
| CT11.01 | Reprovar | Como moderador, reprovar um comentário pela ação do admin | O comentário some da página do texto | Auto |
| CT11.02 | Reaprovar | Aprovar de novo o comentário de CT11.01 | O comentário volta a aparecer | Auto |
| CT11.03 | Filtro | No admin, filtrar comentários por não aprovados | Só os reprovados são listados | Auto |
| CT11.04 | Autorização | Como ana, acessar /admin/ | Redirecionada para a tela de entrada do admin; nenhum conteúdo da moderação é exibido | Auto |

### 3.11 UC13: Gerenciar usuários

| ID | Cenário | Passos e dados | Resultado esperado | Tipo |
| --- | --- | --- | --- | --- |
| CT13.01 | Conceder papel | Pelo admin, incluir bruno no grupo de moderadores | bruno passa a acessar a moderação de comentários | Auto |
| CT13.02 | Desativar | Desativar a conta de bruno e tentar entrar com ela | Autenticação recusada | Auto |
| CT13.03 | RN18 | Como moderador, abrir no admin a própria conta e a de bruno | O formulário mostra só situação da conta, acesso ao admin e grupos, sem campo de superusuário nem permissões avulsas | Auto |
| CT13.04 | RN18 | Como moderador, enviar direto ao servidor uma alteração na conta do superusuário | Erro 403, e a conta não muda | Auto |

## 4 Testes não funcionais

| ID | Objetivo | Como verificar | Critério de aceitação | Tipo |
| --- | --- | --- | --- | --- |
| CTN01 | ONF01 Usabilidade | Percorrer listagem, leitura, cadastro e editor com a tela emulada em 360 pixels de largura | Nenhuma rolagem horizontal; todos os botões e campos alcançáveis | Manual |
| CTN02 | ONF02 Desempenho | Com 500 textos publicados na base, medir o tempo de resposta da listagem, cinco vezes (teste automatizado e medição no servidor de desenvolvimento) | Todas as medições até 2 segundos, e número de consultas que não cresce com a quantidade de textos | Auto |
| CTN03 | ONF03 Segurança | Enviar um formulário por POST sem o token CSRF, como orienta o guia da OWASP (OWASP Foundation, 2020) | Erro 403 | Auto |
| CTN04 | ONF03 Segurança | Buscar o termo ' OR '1'='1 | Tratado como texto comum: nenhum resultado e nenhum erro | Auto |
| CTN05 | ONF03 Segurança | Ver CT05.09 (hash da senha) e CT10.07 (XSS no comentário) | Os dois casos aprovados | Auto |
| CTN06 | ONF04 Autorização | Ver CT08.06, CT08.07, CT09.03, CT10.03, CT11.04, CT13.03 e CT13.04 | Todos os casos aprovados | Auto |
| CTN07 | ONF05 Portabilidade | Rodar python manage.py test em Windows, Linux e macOS; abrir o sistema no Chrome e no Firefox | Testes passam nos três sistemas; telas iguais nos dois navegadores | Manual |
| CTN08 | ONF06 Manutenibilidade | Rodar um verificador de estilo PEP 8 sobre o código | Nenhuma violação | Auto |
| CTN09 | ONF07 Acessibilidade | Percorrer as páginas com formulário (cadastro, entrada, editor, perfil, comentário e busca) conferindo que todo campo tem rótulo associado e que a página declara o idioma | Todo campo tem rótulo; idioma declarado | Auto |
| CTN10 | ONF08 Localização | Publicar um texto às 23h30 no horário de Brasília | A data exibida é a do dia em Brasília, em português, e não a do dia seguinte em UTC | Auto |
| CTN11 | ONF07 Acessibilidade | Navegar pelos formulários só com o teclado e passar as páginas pelo verificador de acessibilidade do navegador | Nenhum erro de contraste; foco visível | Manual |

## 5 Rastreabilidade

| Regra | Descrição resumida | Casos de teste |
| --- | --- | --- |
| RN01 | Rascunho é invisível para quem não é o autor, com 404 | CT01.02, CT02.06, CT02.07 |
| RN02 | Comentário não aprovado só aparece ao moderador | CT02.02, CT11.01 |
| RN03 | Busca no título e no corpo, sem diferenciar maiúsculas | CT03.02, CT03.03 |
| RN04 | Rascunho fora do resultado e da contagem da busca | CT03.10 |
| RN05 | Termo no endereço, preservado na troca de página | CT03.07, CT03.11 |
| RN06 | Senha armazenada com hash PBKDF2 | CT05.09 |
| RN07 | Regras de robustez da senha | CT05.04 a CT05.08 |
| RN08 | Conta nova nasce com papel de autor | CT05.10 |
| RN09 | Autor só altera o que é seu, com verificação no servidor | CT08.06, CT08.07, CT09.03 |
| RN10 | Slug imutável depois da primeira publicação | CT08.10, CT09.04 |
| RN11 | Excluir texto exclui seus comentários | CT08.08 |
| RN12 | Todo texto nasce como rascunho | CT08.01 |
| RN13 | Comentar exige autenticação | CT10.02 |
| RN14 | Comentário nasce aprovado | CT10.01 |
| RN15 | Comentário exibido como texto puro | CT10.07 |
| RN16 | Vínculo do comentário com o autor não é editável | CT10.08 |
| RN17 | Autor pode encerrar os comentários do seu texto | CT10.03, CT10.09 |
| RN18 | Moderador não vê nem concede papel de superusuário | CT13.03, CT13.04 |

| Caso de uso | Aplicação | Auto | Manual | Total |
| --- | --- | --- | --- | --- |
| UC01: Listar posts publicados | posts | 4 | 0 | 4 |
| UC02: Ler post | posts | 7 | 0 | 7 |
| UC03: Buscar post | posts | 11 | 0 | 11 |
| UC05: Cadastrar-se | accounts | 11 | 0 | 11 |
| UC06: Autenticar-se | accounts | 5 | 0 | 5 |
| UC07: Manter perfil | accounts | 4 | 0 | 4 |
| UC08: Manter post | posts | 11 | 0 | 11 |
| UC09: Publicar post | posts | 4 | 0 | 4 |
| UC10: Comentar post | comments | 9 | 0 | 9 |
| UC11: Moderar comentário | comments | 4 | 0 | 4 |
| UC13: Gerenciar usuários | accounts | 4 | 0 | 4 |
| Total |  | 74 | 0 | 74 |

O plano tem 74 casos de teste funcionais (74 automatizados, 0 manuais) e 11 não funcionais (8 automatizados, 3 manuais).

## 6 Resultado da execução da Iteração 2

### 6.1 Ambiente e versão

| Item | Valor |
| --- | --- |
| Data | 4 de novembro de 2026 |
| Versão testada | tag v2 do repositório github.com/ataraxia-ppads/ataraxia-blog (commit ver tag v2) |
| Quem executou | Renan Jordão, com apoio do Claude Code (assistente de IA), em máquina Windows 11 |
| Sistema e software | Windows 11 Pro (10.0.26200), Python 3.14.6, Django 6.1, SQLite |

### 6.2 Verificações executadas

| Verificação | Como | Resultado |
| --- | --- | --- |
| Testes automatizados | python manage.py test | 83 testes, todos aprovados (cerca de 28 s). Eram 57 na Iteração 1. |
| Estilo PEP 8 (CTN08) | python -m pycodestyle accounts posts comments config | Nenhuma violação. |
| Migrações em dia | python manage.py makemigrations --check --dry-run | No changes detected. |
| Verificação do Django | python manage.py check | Nenhum problema encontrado. |
| Instruções do README | Ambiente virtual novo, pip install -r requirements.txt, migrate, carregar_demo e runserver | Seguidas passo a passo. carregar_demo informou "9 textos publicados, 1 rascunho(s)", como o plano espera. Resposta HTTP: página inicial, busca, cadastro, entrada e entrada do admin 200; slug inexistente 404. |

### 6.3 Desempenho (CTN02)

Medição com 509 textos publicados (500 acrescentados aos 9 da demonstração), cinco requisições por rota, no servidor de desenvolvimento. O limite do plano é 2 s.

| Rota | Mínimo | Máximo | Média |
| --- | --- | --- | --- |
| Listagem (página 1) | 0,014 s | 0,112 s | 0,034 s |
| Listagem (página 2) | 0,014 s | 0,015 s | 0,015 s |
| Busca por termo | 0,004 s | 0,005 s | 0,004 s |

### 6.4 Defeitos e divergências

- Nenhum defeito do sistema foi encontrado nesta execução.
- Duas falhas apareceram enquanto os testes novos eram escritos, e as duas eram erro do próprio teste, corrigido na hora: um argumento enviado ao formulário como se fosse campo (CT10.01), e um número de consultas esperado errado (3 em vez de 2, CTN02). Nenhuma indicou problema no código.
- Duas divergências entre plano e sistema foram resolvidas ajustando o plano: CT05.10 e CT11.04 esperavam "acesso negado", e o admin do Django redireciona quem não tem acesso para a própria tela de entrada. O comportamento é correto e a descrição foi corrigida.

### 6.5 Pendências

| Caso | Assunto | Situação |
| --- | --- | --- |
| CTN01 | Usabilidade em 360 px | Exige o navegador com a tela emulada. Pendente para o percurso de Rafaela. |
| CTN07 | Portabilidade | Windows executado. Linux será coberto pela verificação contínua quando o Pull Request da iteração for aberto; macOS e Firefox não foram executados. |
| CTN11 | Contraste e teclado | Exige o verificador de acessibilidade do navegador. Pendente. |
| Percurso de fumaça | Seção 2.8 | Percurso no navegador sobre a versão publicada. Pendente: o sistema ainda não foi publicado em blog.ataraxia.dev. |

## Apêndice A: casos de teste e testes automatizados

Todo teste leva o identificador do caso no nome, para que uma falha aponte direto para o caso de uso.

| Caso | Arquivo | Teste |
| --- | --- | --- |
| CT01.01 | posts/test_fluxos.py | ReadAndListTests.test_ct01_01 |
| CT01.02 | posts/tests.py | ListTests.test_ct01_02 |
| CT01.03 | posts/tests.py | ListTests.test_ct01_03 |
| CT01.04 | posts/tests.py | ListTests.test_ct01_04 |
| CT02.01 | posts/test_fluxos.py | ReadAndListTests.test_ct02_01 |
| CT02.02 | posts/tests.py | DetailTests.test_ct02_02 |
| CT02.03 | posts/test_fluxos.py | ReadAndListTests.test_ct02_03 |
| CT02.04 | posts/test_fluxos.py | ReadAndListTests.test_ct02_04 |
| CT02.05 | posts/tests.py | DetailTests.test_ct02_05 |
| CT02.06 | posts/tests.py | DetailTests.test_ct02_06 |
| CT02.07 | posts/tests.py | DetailTests.test_ct02_07 |
| CT03.01 | posts/test_fluxos.py | SearchFlowTests.test_ct03_01 |
| CT03.02 | posts/tests.py | SearchTests.test_ct03_02 |
| CT03.03 | posts/tests.py | SearchTests.test_ct03_03 |
| CT03.04 | posts/tests.py | SearchTests.test_ct03_04 |
| CT03.05 | posts/test_fluxos.py | SearchFlowTests.test_ct03_05 |
| CT03.06 | posts/tests.py | SearchTests.test_ct03_06 |
| CT03.07 | posts/tests.py | SearchTests.test_ct03_07 |
| CT03.08 | posts/test_fluxos.py | SearchFlowTests.test_ct03_08 |
| CT03.09 | posts/tests.py | SearchTests.test_ct03_09 |
| CT03.10 | posts/tests.py | SearchTests.test_ct03_10 |
| CT03.11 | posts/test_fluxos.py | SearchFlowTests.test_ct03_11 |
| CT05.01 | accounts/tests.py | SignUpTests.test_cadastro_cria_conta_perfil_e_sessao |
| CT05.02 | accounts/tests.py | SignUpTests.test_ct05_02 |
| CT05.03 | accounts/tests.py | SignUpTests.test_ct05_03 |
| CT05.04 | accounts/tests.py | SignUpTests.test_ct05_04 |
| CT05.05 | accounts/tests.py | SignUpTests.test_ct05_05 |
| CT05.06 | accounts/tests.py | SignUpTests.test_ct05_06 |
| CT05.07 | accounts/tests.py | SignUpTests.test_ct05_07 |
| CT05.08 | accounts/tests.py | SignUpTests.test_ct05_08 |
| CT05.09 | accounts/tests.py | SignUpTests.test_ct05_09 |
| CT05.10 | accounts/tests.py | SignUpTests.test_ct05_10 |
| CT05.11 | accounts/test_fluxos.py | FlowTests.test_ct05_11 |
| CT06.01 | accounts/test_fluxos.py | FlowTests.test_ct06_01 |
| CT06.02 | accounts/tests.py | LoginTests.test_ct06_02_e_ct06_03 |
| CT06.03 | accounts/tests.py | LoginTests.test_ct06_02_e_ct06_03 |
| CT06.04 | accounts/tests.py | LoginTests.test_ct06_04 |
| CT06.05 | accounts/test_fluxos.py | FlowTests.test_ct06_05 |
| CT07.01 | accounts/test_fluxos.py | FlowTests.test_ct07_01_ct07_02 |
| CT07.02 | accounts/test_fluxos.py | FlowTests.test_ct07_01_ct07_02 |
| CT07.03 | accounts/tests.py | ProfileTests.test_ct07_03 |
| CT07.04 | accounts/tests.py | ProfileTests.test_ct07_04 |
| CT08.01 | posts/test_fluxos.py | MaintainFlowTests.test_ct08_01 |
| CT08.02 | posts/tests.py | MaintainTests.test_ct08_02 |
| CT08.03 | posts/tests.py | MaintainTests.test_ct08_03 |
| CT08.04 | posts/tests.py | MaintainTests.test_ct08_04 |
| CT08.05 | posts/test_fluxos.py | MaintainFlowTests.test_ct08_05 |
| CT08.06 | posts/tests.py | MaintainTests.test_ct08_06 |
| CT08.07 | posts/tests.py | MaintainTests.test_ct08_07 |
| CT08.08 | posts/tests.py | MaintainTests.test_ct08_08 |
| CT08.09 | posts/test_fluxos.py | MaintainFlowTests.test_ct08_09 |
| CT08.10 | posts/tests.py | MaintainTests.test_ct08_10 |
| CT08.11 | posts/tests.py | MaintainTests.test_ct08_11 |
| CT09.01 | posts/test_fluxos.py | MaintainFlowTests.test_ct09_01 |
| CT09.02 | posts/tests.py | PublishTests.test_ct09_02 |
| CT09.03 | posts/tests.py | PublishTests.test_ct09_03 |
| CT09.04 | posts/tests.py | PublishTests.test_ct09_04 |
| CT10.01 | comments/test_fluxos.py | MainFlowTests.test_ct10_01 |
| CT10.02 | comments/tests.py | CreateTests.test_ct10_02 |
| CT10.03 | comments/tests.py | CreateTests.test_ct10_03 |
| CT10.04 | comments/tests.py | CreateTests.test_ct10_04 |
| CT10.05 | comments/tests.py | CreateTests.test_ct10_05 |
| CT10.06 | comments/tests.py | CreateTests.test_ct10_06 |
| CT10.07 | comments/tests.py | CreateTests.test_ct10_07 |
| CT10.08 | comments/tests.py | CreateTests.test_ct10_08 |
| CT10.09 | posts/test_fluxos.py | MaintainFlowTests.test_ct10_09 |
| CT11.01 | comments/tests.py | ModerationTests.test_ct11_02 |
| CT11.02 | comments/tests.py | ModerationTests.test_ct11_02 |
| CT11.03 | accounts/test_fluxos.py | ModerationFlowTests.test_ct11_03 |
| CT11.04 | accounts/tests.py | AdminPermissionTests.test_ct11_04 |
| CT13.01 | accounts/tests.py | AdminPermissionTests.test_moderador_concede_o_papel_a_outro |
| CT13.02 | accounts/tests.py | AdminPermissionTests.test_ct13_02 |
| CT13.03 | accounts/tests.py | AdminPermissionTests.test_ct13_03 |
| CT13.04 | accounts/tests.py | AdminPermissionTests.test_ct13_04 |
| CTN02 | posts/test_nao_funcionais.py | PerformanceTests.test_ctn02_* |
| CTN03 | comments/tests.py | SecurityTests.test_ctn03 |
| CTN04 | posts/tests.py | SearchTests.test_ctn04 |
| CTN05 | (ver CT05.09 e CT10.07) |  |
| CTN06 | (ver CT08.06, CT08.07, CT09.03, CT10.03, CT11.04, CT13.03, CT13.04) |  |
| CTN08 | .github/workflows/testes.yml | passo "Estilo (PEP 8)" |
| CTN09 | posts/test_nao_funcionais.py | AccessibilityTests.test_ctn09_* |
| CTN10 | posts/tests.py | LocalizationTests.test_ctn10 |

## Referências

- DELAMARO, Márcio Eduardo; MALDONADO, José Carlos; JINO, Mario. Introdução ao teste de software. 2. ed. Rio de Janeiro: Elsevier, 2016.
- DJANGO SOFTWARE FOUNDATION. Django documentation: versão 6.1. [S.l.]: Django Software Foundation, 2026. Disponível em: <https://docs.djangoproject.com/en/6.1/>. Acesso em: 14 out. 2026.
- IEEE. IEEE Std 829-2008: IEEE standard for software and system test documentation. New York: IEEE, 2008.
- ISO. ISO/IEC/IEEE 29119-3:2021: software and systems engineering: software testing: part 3: test documentation. Geneva: ISO, 2021.
- MYERS, Glenford J.; SANDLER, Corey; BADGETT, Tom. The art of software testing. 3. ed. Hoboken: John Wiley & Sons, 2011.
- OWASP FOUNDATION. Web Security Testing Guide: versão 4.2. [S.l.]: OWASP Foundation, 2020. Disponível em: <https://owasp.org/www-project-web-security-testing-guide/>. Acesso em: 14 out. 2026.
- PRESSMAN, Roger S.; MAXIM, Bruce R. Engenharia de software: uma abordagem profissional. 8. ed. Porto Alegre: AMGH, 2016.
- SOMMERVILLE, Ian. Engenharia de software. 9. ed. São Paulo: Pearson Prentice Hall, 2011.

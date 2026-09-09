# Diagramas de sequência de projeto

Os diagramas de sequência de sistema mostram o que o usuário pede e o que o
sistema responde, com o sistema fechado numa caixa só. Aqui a caixa é aberta: os
mesmos fluxos aparecem com as classes que vão executá-los, na ordem em que
trocam mensagem.

Os participantes seguem sempre o mesmo caminho, que é o do Django:

```mermaid
flowchart LR
    navegador --> urls[urls.py]
    urls --> View
    View --> Form
    Form --> Model
    Model --> banco[(banco)]
    View --> Template
```

**Figura 20 — Caminho de uma requisição**

`urls.py` aparece porque é ele que escolhe a view a partir do endereço, e o
endereço é parte do desenho: categoria e tag são resolvidas por slug, e o texto
também.

Cinco diagramas, um por caso de uso principal, na mesma ordem do capítulo de
casos de uso.

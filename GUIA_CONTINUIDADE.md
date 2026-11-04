# GUIA DE CONTINUIDADE — MODERNIZAÇÃO DO SUPERMARKET RECEIPT

## 1. Objetivo do trabalho

Modernizar incrementalmente o sistema legado Supermarket Receipt, utilizando boas práticas de Engenharia de Software, refatoração, padrões de projeto, testes automatizados e análise de segurança.

O objetivo não é reescrever o sistema do zero. É compreender o funcionamento original, preservar suas regras de negócio e melhorar sua estrutura de forma segura.

A implementação deve partir do código original do repositório oficial, na versão Python com pytest (`python_pytest`).

## 2. Regras obrigatórias

1. Não substituir o código original por uma solução pronta.
2. Não utilizar testes preexistentes como substitutos dos testes de caracterização desenvolvidos pelo grupo.
3. Executar e registrar o comportamento original antes de modificar o código.
4. Criar testes automatizados com pytest.
5. Preservar as promoções e regras de negócio existentes.
6. Aplicar pelo menos dois padrões de projeto, justificando sua utilização.
7. Implementar a promoção de combos sem conceder descontos indevidos.
8. Executar Bandit, pip-audit e Safety antes e depois das alterações.
9. Registrar evidências reais de execução, testes e auditorias.
10. Manter o projeto executável e documentado.

## 3. Nova regra de negócio: combos promocionais

Um combo é formado por uma quantidade definida de produtos.

Quando todos os produtos necessários para formar um combo forem comprados, os itens participantes daquele combo recebem 10% de desconto.

Exemplos:

- 1 escova + 1 pasta: os dois produtos recebem 10% de desconto.
- 2 escovas + 1 pasta: somente uma escova e uma pasta recebem desconto.
- 2 escovas + 2 pastas: os quatro produtos recebem desconto, formando dois combos.
- 1 escova sem pasta: nenhum desconto de combo.

O sistema deve evitar:
- Descontar produtos que não completam um combo.
- Descontar duas vezes o mesmo item.
- Alterar indevidamente as promoções antigas.

O grupo deve descobrir como as ofertas atuais funcionam antes de definir como os combos vão coexistir com elas.

## 4. Ordem obrigatória de execução

### Etapa 1 — Conhecer o sistema
- Ler o README original.
- Identificar carrinho, produtos, ofertas, descontos e recibos.
- Entender as classes e suas responsabilidades.
- Registrar a estrutura do projeto.

### Etapa 2 — Execução inicial
- Preparar o ambiente Python.
- Instalar as dependências.
- Executar os testes disponíveis.
- Executar o sistema original, se houver fluxo de execução.
- Registrar comandos, versões, resultados e erros.

### Etapa 3 — Diagnóstico técnico
Identificar problemas reais no código, como:
- Condicionais extensas.
- Código duplicado.
- Alto acoplamento.
- Responsabilidades misturadas.
- Dificuldade de testar ou adicionar novas promoções.

Todo problema apontado deve estar relacionado a um arquivo, trecho ou comportamento concreto.

### Etapa 4 — Requisitos
Documentar requisitos funcionais (RF) e não funcionais (RNF), incluindo:
- Promoções antigas.
- Cálculo de descontos.
- Geração de recibos.
- Formação de combos.
- Tratamento de quantidades incompletas e excedentes.

Cada requisito precisa ter um critério de aceitação verificável.

### Etapa 5 — Plano de contingência
Definir:
- Ordem segura das alterações.
- Riscos de regressão.
- Estratégia de testes.
- Critérios para aceitar cada mudança.
- Como retornar à versão anterior se algo quebrar.
- Interfaces e comportamentos que precisam ser preservados.

### Etapa 6 — Testes de caracterização
Criar testes que registrem o comportamento original antes da refatoração.

Cobrir:
- Carrinho sem promoção.
- Promoções existentes.
- Descontos.
- Quantidades e limites.
- Cálculo e conteúdo dos recibos.
- Combinações relevantes de ofertas.

### Etapa 7 — Segurança inicial
Executar:
- Bandit.
- pip-audit.
- Safety.

Registrar versões, comandos, resultados e limitações do ambiente.

### Etapa 8 — Refatoração
Refatorar em pequenas etapas, executando os testes após cada alteração.

Aplicar pelo menos dois padrões de projeto adequados ao código encontrado. Strategy e Factory Method são possibilidades, mas a escolha deve ser justificada pelo problema real.

Documentar:
- Problema original.
- Solução adotada.
- Classes envolvidas.
- Antes e depois.
- Testes relacionados.

### Etapa 9 — Implementação dos combos
Implementar a nova promoção de 10%, respeitando as regras de formação de combos e a compatibilidade com as promoções antigas.

### Etapa 10 — Testes de regressão
Testar:
- Combo completo.
- Combo incompleto.
- Mais de um combo.
- Produtos excedentes.
- Coexistência com promoções antigas.
- Ausência de desconto duplicado.

### Etapa 11 — Segurança final
Executar novamente Bandit, pip-audit e Safety.

Comparar os resultados antes e depois, explicando os alertas encontrados e as correções realizadas ou justificadamente não realizadas.

### Etapa 12 — Entrega
Preparar:
- Código final.
- Testes automatizados.
- README.
- Diagnóstico.
- Requisitos.
- Plano de contingência.
- Documentação dos padrões.
- Relatório de segurança.
- Evidências.
- Apresentação de 10 a 15 minutos.

## 5. Orientações para outras IAs

Qualquer IA que ajudar no projeto deve:

1. Ler este guia e o PDF original da atividade antes de propor alterações.
2. Inspecionar o código real antes de recomendar refatorações.
3. Não inventar nomes de classes, métodos, arquivos ou resultados de execução.
4. Não presumir que os testes passaram sem executar ou receber evidências.
5. Não modificar regras de negócio existentes sem justificativa.
6. Não implementar padrões de projeto artificialmente apenas para cumprir quantidade.
7. Explicar cada alteração, indicando os arquivos afetados e como testar.
8. Preferir mudanças pequenas, rastreáveis e reversíveis.
9. Atualizar a documentação e os testes junto com as alterações.
10. Sinalizar claramente o que ainda não foi realizado.

Se faltar informação, pedir o arquivo, código, log ou resultado necessário antes de assumir.

## 6. Critério de conclusão

O trabalho só deve ser considerado concluído quando:
- O sistema final executar corretamente.
- Os testes de comportamento legado e os novos testes passarem.
- Os combos respeitarem todos os casos previstos.
- Dois ou mais padrões estiverem implementados e justificados.
- As três ferramentas de segurança tiverem sido executadas antes e depois.
- A documentação e as evidências estiverem completas.
- O grupo conseguir explicar tecnicamente as decisões na apresentação.
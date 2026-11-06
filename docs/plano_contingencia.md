# Plano de Contingência

## 1. Objetivo

Definir ações preventivas e procedimentos de recuperação para reduzir os riscos durante a modernização incremental do sistema legado de checkout de supermercado.

O plano tem como objetivo preservar as funcionalidades existentes, evitar alterações acidentais nas regras de negócio, garantir a integridade dos cálculos e permitir a recuperação de uma versão estável caso ocorram problemas durante o desenvolvimento.

Também estabelece medidas para reduzir riscos relacionados à implementação da nova promoção de combos, à aplicação de descontos e à introdução de alterações arquiteturais.

## 2. Principais riscos e ações preventivas

| Risco | Impacto | Prevenção |
|---|---|---|
| Alterar o cálculo de preços ou descontos existentes | Valores incorretos no caixa e divergência nos recibos | Manter os testes de caracterização e executar a suíte de regressão após cada alteração relevante. |
| Modificar acidentalmente comportamentos peculiares do sistema legado | Perda de compatibilidade com o comportamento original | Consultar os testes de caracterização e preservar os resultados documentados, salvo alterações intencionais e justificadas. |
| Aplicar descontos indevidos nos combos | Prejuízo financeiro e erro no recibo | Testar combos completos, incompletos, múltiplos combos e produtos excedentes. |
| Acumular descontos incompatíveis | Concessão de descontos duplicados sobre as mesmas unidades | Aplicar a regra de exclusividade por unidade e criar testes específicos para a interação entre promoções. |
| Contabilizar uma mesma unidade em mais de um combo | Desconto duplicado e cálculo incorreto | Controlar as unidades participantes de cada combo e validar a quantidade utilizada. |
| Alterar contratos públicos durante a refatoração | Falhas em componentes que dependem das interfaces existentes | Preservar assinaturas, propriedades e comportamentos públicos protegidos pelos testes. |
| Refatorar muitas classes simultaneamente | Dificuldade para localizar erros e identificar a origem de regressões | Realizar alterações pequenas, incrementais e isoladas por funcionalidade. |
| Introduzir falhas durante a refatoração | Sistema deixa de funcionar corretamente | Executar os testes automatizados após cada mudança relevante. |
| Introduzir vulnerabilidades ou dependências inseguras | Riscos de segurança para a aplicação | Executar Bandit, pip-audit e Safety antes e depois das alterações. |
| Perder alterações ou comprometer a versão estável | Retrabalho e perda de progresso | Utilizar Git, manter branches organizadas e realizar commits pequenos e identificáveis. |
| Introduzir conflitos durante a integração das branches | Perda de alterações ou inconsistências no código | Integrar funcionalidades por meio de Pull Requests e revisar os conflitos antes da conclusão do merge. |

## 3. Procedimento em caso de falha

Se uma alteração provocar erros, resultados incorretos ou falhas nos testes, deverão ser adotados os seguintes procedimentos:

1. Interromper novas alterações na funcionalidade afetada.
2. Identificar o arquivo, método ou componente relacionado ao problema.
3. Executar os testes automatizados para localizar a falha.
4. Verificar se o problema já existia no comportamento legado ou se foi introduzido pela alteração.
5. Comparar o comportamento atual com os resultados registrados nos testes de caracterização.
6. Verificar se houve alteração indevida em contratos públicos, cálculos, descontos ou formatação do recibo.
7. Corrigir a implementação e executar novamente os testes.
8. Caso não seja possível corrigir o problema de maneira segura, retornar ao último estado estável utilizando o Git.
9. Registrar o problema identificado, sua causa, a solução adotada e os testes realizados após a recuperação.

Falhas relacionadas à promoção de combos deverão ser investigadas considerando especialmente:

- Quantidade de combos completos formados.
- Produtos e unidades participantes de cada combo.
- Produtos excedentes.
- Aplicação dos descontos individuais nas unidades não utilizadas nos combos.
- Possibilidade de descontos duplicados.
- Correção do valor final e da apresentação do recibo.

## 4. Estratégia de rollback

O Git será utilizado para manter o histórico das alterações e permitir a recuperação de versões anteriores do projeto.

A organização das branches seguirá a estratégia definida pelo grupo:

- `main`: branch principal, destinada à versão estável do projeto.
- `develop`: branch de integração das funcionalidades.
- `feature/*`: branches utilizadas para desenvolver funcionalidades específicas.

Antes de alterações relevantes, deverá existir um commit que represente um estado funcional e testado do projeto.

As funcionalidades deverão ser desenvolvidas em branches próprias, criadas a partir de `develop`, e integradas por meio de Pull Requests após revisão e validação.

Se uma alteração comprometer o funcionamento do sistema:

1. Identificar o commit responsável pelo problema.
2. Verificar se a alteração já foi integrada à branch de destino.
3. Caso tenha sido integrada, utilizar `git revert` para desfazer o commit problemático, preservando o histórico.
4. Caso ainda esteja em uma branch de desenvolvimento, corrigir ou descartar as alterações dessa branch sem comprometer as demais funcionalidades.
5. Executar novamente os testes automatizados.
6. Confirmar que o projeto voltou a apresentar comportamento estável.

O comando `git revert` deverá ser utilizado preferencialmente para desfazer alterações já compartilhadas, evitando a reescrita do histórico de branches compartilhadas.

Durante o desenvolvimento, também serão realizados testes de regressão para verificar se as funcionalidades antigas continuam funcionando após cada integração relevante.

## 5. Invariantes de negócio

As seguintes condições deverão permanecer verdadeiras durante e após a modernização:

- Os preços dos produtos devem continuar seguindo as regras de cálculo do sistema.
- A quantidade registrada no carrinho deve corresponder às quantidades adicionadas.
- O recibo deve considerar os produtos e descontos registrados.
- As promoções existentes devem preservar os comportamentos protegidos pelos testes de caracterização.
- Os contratos públicos existentes devem permanecer compatíveis.
- Um combo incompleto não pode gerar desconto.
- Somente unidades pertencentes a combos completos podem receber o desconto de combo.
- Produtos excedentes não podem receber desconto de combo indevidamente.
- Uma mesma unidade não pode participar de mais de um combo na mesma compra.
- Uma mesma unidade não pode receber simultaneamente o desconto de combo e outra promoção incompatível.
- Unidades excedentes devem continuar elegíveis às promoções antigas, respeitando as regras originais dessas ofertas.
- A aplicação dos descontos não pode contabilizar repetidamente uma mesma unidade.
- A implementação dos combos não deve alterar indevidamente os cálculos e descontos das funcionalidades existentes.

## 6. Validação após recuperação

Após qualquer correção, integração relevante ou rollback, deverão ser realizadas as seguintes verificações:

- Executar todos os testes automatizados.
- Confirmar a aprovação dos testes de caracterização do comportamento legado.
- Conferir os cálculos de preços e descontos.
- Verificar a geração e a formatação do recibo.
- Validar os cenários de combos completos e incompletos.
- Verificar a formação de múltiplos combos.
- Conferir o tratamento de produtos excedentes.
- Validar a regra de exclusividade por unidade.
- Verificar a interação entre as promoções antigas e a nova promoção de combos.
- Executar as ferramentas de segurança quando houver alterações relevantes no código ou nas dependências.
- Registrar os resultados das verificações nas evidências do projeto.

A modernização somente será considerada estável quando os testes forem aprovados, as regras de negócio estiverem preservadas e as novas funcionalidades apresentarem os resultados esperados.

## 7. Registro das ocorrências

Problemas relevantes identificados durante a modernização deverão ser documentados para manter a rastreabilidade das decisões e das correções realizadas.

O registro deverá conter, quando aplicável:

- Descrição do problema.
- Arquivo ou funcionalidade afetada.
- Causa identificada.
- Impacto no sistema.
- Solução adotada.
- Commit ou Pull Request relacionado.
- Testes executados após a correção.
- Resultado da validação.

Esse registro permitirá acompanhar a evolução do projeto e fornecer evidências das medidas adotadas para preservar a estabilidade do sistema.
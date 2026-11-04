# Plano de Contingência

## 1. Objetivo

Definir ações para reduzir os riscos durante a modernização do sistema legado de checkout, garantindo que as funcionalidades existentes sejam preservadas e que seja possível recuperar uma versão estável caso ocorram problemas.

## 2. Principais riscos e ações preventivas

| Risco | Impacto | Prevenção |
|---|---|---|
| Alterar o cálculo de preços ou descontos existentes | Valores incorretos no caixa | Criar testes de caracterização antes das alterações. |
| Aplicar descontos indevidos nos combos | Prejuízo financeiro e erro no recibo | Testar combos completos, incompletos e produtos excedentes. |
| Acumular descontos incompatíveis | Desconto duplicado no mesmo item | Definir e testar regras de prioridade e coexistência. |
| Refatorar muitas classes simultaneamente | Dificuldade para localizar erros | Realizar alterações pequenas e incrementais. |
| Introduzir falhas durante a refatoração | Sistema deixa de funcionar | Executar os testes após cada mudança relevante. |
| Introduzir vulnerabilidades ou dependências inseguras | Risco de segurança | Executar Bandit, pip-audit e Safety antes e depois das alterações. |
| Perder alterações ou comprometer a versão estável | Retrabalho e perda de progresso | Utilizar Git e manter commits pequenos e identificáveis. |

## 3. Procedimento em caso de falha

Se uma alteração provocar erros ou resultados incorretos:

1. Interromper novas alterações.
2. Identificar o arquivo e a funcionalidade afetada.
3. Executar os testes automatizados para localizar a falha.
4. Comparar o comportamento atual com os resultados registrados antes da refatoração.
5. Corrigir a alteração e executar novamente os testes.
6. Caso não seja possível corrigir rapidamente, retornar ao último commit estável utilizando o Git.
7. Registrar o problema e a solução adotada.

## 4. Estratégia de rollback

O Git será utilizado para manter o histórico das alterações e permitir a recuperação de versões anteriores.

Antes de mudanças relevantes, será criado um commit com o estado estável do projeto. Se uma alteração comprometer o funcionamento, poderá ser revertida com `git revert`, preservando o histórico.

Durante o desenvolvimento, também serão executados testes de regressão para verificar se as funcionalidades antigas continuam funcionando.

## 5. Invariantes de negócio

As seguintes condições deverão permanecer verdadeiras durante e após a modernização:

- O preço dos produtos deve continuar sendo calculado corretamente.
- A quantidade registrada no carrinho deve corresponder à quantidade comprada.
- O total do recibo deve considerar os preços e descontos aplicáveis.
- As promoções existentes devem preservar seu comportamento esperado.
- Um combo incompleto não pode gerar desconto.
- Produtos excedentes não podem receber desconto de combo indevidamente.
- Um mesmo item não pode receber descontos incompatíveis ou ser contabilizado duas vezes no mesmo combo.

## 6. Validação após recuperação

Após qualquer correção ou rollback:

- Executar todos os testes automatizados.
- Conferir os cálculos de preços e descontos.
- Verificar a geração do recibo.
- Validar novamente os cenários de combos.
- Executar as ferramentas de segurança quando houver alterações relevantes nas dependências ou no código.

A modernização somente será considerada estável quando os testes forem aprovados e as regras de negócio forem preservadas.
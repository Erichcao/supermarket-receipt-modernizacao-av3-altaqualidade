# Lições aprendidas

## Contexto

A modernização foi conduzida de forma incremental sobre um sistema legado de checkout. A principal dificuldade não foi somente adicionar a promoção de combos, mas compreender e preservar comportamentos existentes que nem sempre eram intuitivos.

## Lições técnicas

- **Caracterização antes da refatoração:** testes de comportamento legado ajudam a identificar contratos e particularidades que poderiam ser alterados acidentalmente. A evidência histórica disponível registra um teste executado no código original; os demais testes de caracterização integram a suíte final e não são apresentados como execução pré-refatoração.
- **Separação por responsabilidade:** encapsular cálculos individuais em estratégias e centralizar sua instanciação tornou as regras promocionais mais localizadas. A Simple Factory ainda exige atualizar seu mapeamento quando uma nova estratégia individual é criada.
- **Combos exigem controle de unidades:** reservar as quantidades utilizadas impede que a mesma unidade receba descontos incompatíveis. As unidades excedentes podem continuar participando das promoções individuais.
- **Decisões de prioridade precisam ser explícitas:** os combos são processados antes das ofertas individuais; combos sobrepostos seguem a ordem de cadastro. A implementação não busca automaticamente a maior economia para o cliente.
- **Cobertura não é sinônimo de qualidade absoluta:** a cobertura final foi de 99% (210 de 213 instruções do código de produção em `src/`). As três instruções não cobertas correspondem a duas proteções de acesso ao banco de dados em `catalog.py` e à declaração do método abstrato `PromotionStrategy.calculate`. Esse resultado demonstra ampla execução dos caminhos medidos, mas não substitui revisão, testes de aceitação ou análise de regras de negócio.
- **Auditorias têm escopo limitado:** Bandit, pip-audit e Safety não substituem revisão manual nem garantem ausência total de vulnerabilidades. Os resultados refletem os ambientes, versões, bases e escopos registrados.

## Limitações e decisões

A estratégia de combo é implementada em uma classe própria, mas não herda da abstração PromotionStrategy; o ShoppingCart instancia essa classe diretamente. O DIP, portanto, foi aplicado parcialmente e essa limitação foi mantida documentada, sem ampliar o escopo da refatoração no encerramento da atividade.

A comparação das auditorias antes/depois possui diferenças de ambiente e escopo, especialmente no Safety. Os relatórios são apresentados com essas limitações, sem interpretar alertas ignorados como vulnerabilidades corrigidas.

## Próximas melhorias possíveis

Em uma evolução futura, seria possível abstrair também o processamento dos combos, rever a dependência do carrinho em relação às classes concretas e introduzir uma política configurável para priorização de ofertas. Essas melhorias não foram tratadas como requisitos obrigatórios desta entrega.

# Segurança: comparação antes e depois

**Projeto:** Supermarket Receipt – Modernização de Software
**Disciplina:** Alta Qualidade de Software (SENAI CIMATEC)
**Branch da última auditoria:** `fix/dependency-hygiene`

Este documento registra os resultados das três ferramentas de auditoria (Bandit, pip-audit e Safety) em três momentos, as correções aplicadas e as limitações de comparação.

---

## 1. Resumo

| Ferramenta | Antes (relatório inicial) | Intermediário | Final |
|---|---|---|---|
| Bandit | 133 linhas, 0 problemas | não executado | 291 linhas, 0 problemas, 0 arquivos ignorados |
| pip-audit | Nenhuma vulnerabilidade conhecida | não executado | Nenhuma vulnerabilidade conhecida (versões fixadas) |
| Safety | 80 dependências, 14 alertas, 14 ignorados | 29 dependências, 1 alerta, 1 ignorado | 29 dependências, 0 alertas, 0 correções sugeridas |

**Conclusão curta:** as ferramentas não apontaram vulnerabilidades no código-fonte (`src`). Os alertas do Safety estavam em dependências e no ambiente de desenvolvimento, e foram tratados com fixação de versões, isolamento das ferramentas de auditoria e atualização do `pip`.

---

## 2. O que foi encontrado e o que foi feito

### 2.1. `pytest` sem versão fixada (1 alerta no relatório inicial)

- **Alerta:** `SFTY-20260122-20373`, faixa afetada `<9.0.3`, política `unpinned-specification`.
- **Causa:** o `requirements.txt` não fixava versões, o que permitia instalar uma versão afetada.
- **Correção:** `requirements.txt` com versões exatas:

```text
approvaltests==20.0.1
coverage==7.17.2
pytest==9.2.0
pytest-approvaltests==0.2.4
```

- **Verificação:** no scan final, `pytest==9.2.0` aparece sem vulnerabilidades conhecidas, tanto no `requirements.txt` quanto no `.venv`.

### 2.2. `filelock` (13 alertas no relatório inicial)

- **Alertas:** 13 identificadores, versão 3.32.7, política `environment-dependency`.
- **Causa:** o `filelock` não faz parte do `requirements.txt`. Ele entrou no ambiente virtual do projeto como dependência indireta quando o Safety foi instalado ali.
- **Correção:** o `.venv` do projeto foi recriado apenas com o `requirements.txt`, e as ferramentas de auditoria (Bandit, pip-audit, Safety) passaram a rodar em um ambiente separado (`auditoria-venv`), fora do repositório.
- **Verificação:** o `pip list` do `.venv` recriado não contém `filelock`, e os relatórios novos não o citam.

### 2.3. `pip` desatualizado (1 alerta no scan intermediário)

- **Alerta:** `SFTY-20261020-17374`, `pip==26.2.1`, faixa afetada `>=19.1,<26.2.2`, ignorado pela política `environment-dependency`.
- **Causa:** o `pip` é ferramenta do ambiente, não está no `requirements.txt`.
- **Correção:** `python -m pip install --upgrade pip` no `.venv` do projeto, que passou para a versão 26.3.
- **Verificação:** o scan final não lista mais nenhum alerta.
- **Observação:** como o `pip` não está no `requirements.txt`, essa correção vale para o ambiente em que foi aplicada. O README orienta a atualizar o `pip` antes de instalar as dependências.

---

## 3. Detalhes por ferramenta (execução final)

### Bandit

- Escopo: diretório `src`.
- Resultado: `No issues identified`, 291 linhas de código, 0 arquivos ignorados.
- Interpretação: nenhum padrão inseguro foi sinalizado pelas regras da ferramenta. Isso não prova ausência total de falhas.

### pip-audit

- Comando: `pip-audit -r requirements.txt -f columns`.
- Resultado: `No known vulnerabilities found`.
- Observação: a saída contém um aviso do módulo `venv` sobre o caminho da pasta temporária no Windows (nome curto e nome completo do mesmo diretório). O aviso não afeta o resultado.
- Interpretação: nenhuma vulnerabilidade conhecida nas versões exatas declaradas.

### Safety

- Versão da ferramenta: 3.8.1, política padrão (`Scan policy: None, using Safety CLI default policies`).
- Escopo: `requirements.txt` e `.venv\pyvenv.cfg` do projeto.
- Resultado: 29 dependências testadas, 0 problemas de segurança, 0 correções sugeridas.
- Interpretação: nenhuma das 29 dependências analisadas teve alerta na base do Safety na data da execução.

---

## 4. Evidências

Arquivos na pasta `evidencias/`:

| Arquivo | Conteúdo |
|---|---|
| `bandit_antes.txt` / `bandit_depois.txt` | Execuções do relatório inicial e da modernização |
| `bandit_final.txt` | Execução final, 291 linhas, 0 problemas |
| `pip_audit_antes.txt` / `pip_audit_depois.txt` | Execuções do relatório inicial |
| `pip_audit_final.txt` | Execução final com versões fixadas |
| `safety_antes.json` / `safety_depois.json` | Relatórios com 14 alertas ignorados |
| `safety_intermediario_pip_26.2.1.json` | Scan com 1 alerta ignorado (`pip` 26.2.1), preservado como registro do processo |
| `safety_final.json` | Scan final, 0 alertas |

---

## 5. Limitações e transparência

1. **Escopos diferentes.** O Safety inicial analisou 80 dependências, incluindo pacotes que entraram no ambiente por causa da instalação do próprio Safety. O scan final analisou 29, porque as ferramentas de auditoria ficaram fora do ambiente do projeto. A redução do número de dependências testadas é consequência da mudança de escopo, e não de remoção de pacotes do projeto.
2. **Ambientes diferentes.** O relatório inicial foi gerado em outro clone no Windows e a segunda execução no Ubuntu. A execução final foi no Windows 11, com as ferramentas de auditoria em Python 3.14.7. As comparações devem ser lidas pelos pacotes, identificadores e classificações, e não como um experimento em ambientes idênticos.
3. **Bandit e Python.** O Bandit analisa o código-fonte sem executá-lo, então a versão do Python do ambiente de auditoria não invalida o resultado.
4. **Ignorado não significa corrigido.** Nos relatórios iniciais, todos os alertas estavam ignorados por política. A melhoria só é afirmada porque o relatório final foi gerado depois das correções e não lista mais nenhum alerta.
5. **Resultado limitado ao momento.** As bases de vulnerabilidades mudam com o tempo. O resultado vale para a data e a versão das ferramentas registradas (Safety 3.8.1, execução de 12/11/2026).
6. **Escopo das ferramentas.** As ferramentas não substituem testes funcionais, revisão manual ou análise dinâmica. Não foram avaliadas autenticação, autorização ou implantação em produção.
7. **Não afirmamos** que o código-fonte tinha vulnerabilidades corrigidas. Nenhuma ferramenta apontou problemas em `src`, antes ou depois.

---

## 6. Como reproduzir (Windows / PowerShell)

```powershell
# Ambiente do projeto (somente dependências do projeto)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -v
deactivate

# Ambiente separado para as ferramentas de auditoria (fora do repositório)
cd ..
python -m venv auditoria-venv
.\auditoria-venv\Scripts\Activate.ps1
python -m pip install --upgrade pip bandit pip-audit safety
cd supermarket-receipt-modernizacao-av3-altaqualidade

bandit -r src -f txt -o evidencias\bandit_final.txt
pip-audit -r requirements.txt -f columns 2>&1 | Out-File -Encoding utf8 evidencias\pip_audit_final.txt
safety scan --target . --save-as json evidencias\safety_final.json
```

O Safety exige uma conta gratuita na primeira execução.

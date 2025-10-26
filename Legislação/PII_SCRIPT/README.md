# 🛡️ PII Scanner

**Auditoria de Dados Pessoais em APIs (Python)**

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

---

Ferramenta de auditoria de segurança para varredura de endpoints de APIs (especialmente Django Rest Framework) em busca de Informações de Identificação Pessoal (PII) sensíveis: **CPF, e-mails, telefones e endereços físicos**.

Gera um **relatório HTML colorido** por risco, com todos os valores mascarados e aviso de confidencialidade.

---

## ✨ Funcionalidades

- **Requisições HTTP**: Faz requisições GET à URL fornecida.
- **Autenticação**: Suporte a Bearer Token (padrão DRF).
- **Varredura Recursiva**: Percorre JSON aninhado (listas/dicionários).
- **Identificação de PII**:
	- **CPF**: Detecta padrão e valida matematicamente.
	- **E-mail**: Detecta padrão.
	- **Telefone (BR)**: Detecta padrões com/sem DDD, 8 ou 9 dígitos (Suspeito).
	- **Endereço Físico**: Detecta termos comuns de endereçamento (Suspeito).
- **Relatório HTML**:
	- Sumário executivo e estatísticas.
	- Classificação por risco: Confirmado (vermelho) e suspeito (amarelo).
	- **Mascaramento de dados**: Todos os valores PII mascarados (ex: 123***45).
	- **Aviso de confidencialidade**.
- **Interface CLI**: Uso simples via argparse.

---

## ⚙️ Instalação

Requer Python 3.7+ e a biblioteca `requests`:

```bash
pip install requests
```

---

## � Como Usar

Salve o script como `pii_scanner.py` e execute pelo terminal:

### 1. Endpoint Protegido (com Token)

```bash
python pii_scanner.py https://api.exemplo.com/v1/usuarios/ --token SEU_TOKEN_AQUI
```

### 2. Endpoint Público (sem Token)

```bash
python pii_scanner.py http://127.0.0.1:8000/api/dados_publicos/
```

### 3. Ajuda

```bash
python pii_scanner.py -h
```

---

## 📊 Saída e Relatório

- Log detalhado dos achados no terminal (valores completos).
- Gera `pii_report.html` no mesmo diretório.
- Exemplo de relatório: [`pii_report_example.html`](./pii_report_example.html)
- O caminho absoluto do relatório é exibido ao final:

```
*** RELATÓRIO HTML GERADO ***
O relatório foi salvo em: /caminho/completo/para/pii_report.html
```

> **Atenção:** Os valores no HTML estão mascarados para segurança. Use o campo "Path" para localizar o dado na API.

---

## 🔬 Tipos de PII e Classificação de Risco

| Categoria         | Descrição da Verificação                                 | Status no Relatório                | Cor no Relatório |
|-------------------|----------------------------------------------------------|------------------------------------|------------------|
| E-mail            | Padrão encontrado                                        | Confirmado/Válido                  | Vermelho         |
| CPF               | 11 dígitos, validação matemática OK                      | CPF VÁLIDO (Matemática OK)         | Vermelho         |
| CPF Suspeito      | 11 dígitos, validação matemática FALHOU                  | CPF suspeito (11 dígitos)          | Amarelo          |
| Telefone          | Padrão BR 10 ou 11 dígitos                               | Telefone suspeito                  | Amarelo          |
| Endereço Físico   | Termos de endereço (Rua, CEP, Nº) detectados            | Endereço Físico suspeito           | Amarelo          |

---

## 📤 Exportação

O relatório HTML pode ser facilmente importado em planilhas para análise adicional.

---

## ⚠️ Observações de Segurança

- O script detecta padrões, mas não garante 100% de precisão. Sempre revise os achados suspeitos.
- O log do terminal exibe valores completos para depuração. Execute em ambiente seguro.
- O relatório HTML é seguro: todos os valores PII estão mascarados.

---

## 📄 Licença

MIT. Veja o arquivo [LICENSE](LICENSE).
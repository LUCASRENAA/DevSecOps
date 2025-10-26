## 📝 Aula 06: Governança, Conformidade (LGPD/ISO 27001) e Auditoria de PII

Esta aula encerrou o ciclo de DevSecOps, movendo o foco para os requisitos de **Conformidade (Compliance)** e **Privacidade de Dados**. Exploramos a importância de legislações como a LGPD e padrões como a ISO 27001, culminando na apresentação de uma ferramenta prática de auditoria de Informações de Identificação Pessoal (PII).

-----

## 🏛️ Conformidade e Governança em DevSecOps

A segurança moderna vai além de evitar *exploits*; ela deve garantir que a aplicação cumpra leis e padrões internacionais sobre proteção de dados.

### 1\. Lei Geral de Proteção de Dados (LGPD)

  * **Foco:** Regulamentação da coleta, uso, processamento e armazenamento de dados pessoais no Brasil.
  * **Relevância para DevSecOps:** Exige que a segurança seja incorporada "desde o design" (*Privacy by Design*). Isso significa que as pipelines de segurança (SAST/DAST/SCA) e os processos de *Threat Modeling* devem priorizar a proteção dos dados pessoais.
  * **PII (Personally Identifiable Information):** Qualquer informação que possa ser usada para identificar, contatar ou localizar uma pessoa específica (ex: Nome, CPF, E-mail).

### 2\. ISO/IEC 27001

  * **Foco:** Padrão internacional para **Sistemas de Gestão de Segurança da Informação (SGSI)**.
  * **Relevância para DevSecOps:** Define os requisitos para estabelecer, implementar, manter e melhorar continuamente um SGSI.
  * **Contribuição:** Ajuda a formalizar processos como Code Review, gestão de vulnerabilidades e a resposta a incidentes, garantindo que toda a operação de desenvolvimento e segurança siga um *framework* reconhecido de alto nível.

-----

## 🕵️‍♂️ PII Scanner: Auditoria de Dados Pessoais em APIs

O `PII Scanner` é uma ferramenta desenvolvida em Python para auxiliar na auditoria de conformidade, agindo como um **scanner dinâmico focado em privacidade**. Ele simula um testador que acessa os *endpoints* da API para identificar a exposição acidental ou desnecessária de dados PII.

### 🎯 Objetivo da Ferramenta

A ferramenta visa responder à pergunta crucial de conformidade: **Nossos *endpoints* de API estão expondo dados pessoais (PII) de forma inadequada, violando a LGPD?**

### ✨ Funcionalidades Principais

| Categoria | Funcionalidade | Relevância para Conformidade (LGPD) |
| :--- | :--- | :--- |
| **Varredura Dinâmica** | Faz requisições `GET` em APIs (incluindo autenticadas via Bearer Token). | Simula o acesso de um sistema ou usuário logado para verificar a real exposição dos dados. |
| **Detecção de PII** | Varre JSON aninhado em busca de padrões de CPF (com validação matemática), E-mails, Telefones e Endereços Físicos. | Ajuda a garantir que apenas dados estritamente necessários sejam retornados pela API (Princípio da Minimização de Dados). |
| **Relatório Seguro** | Gera relatório HTML colorido com sumário executivo. Todos os valores PII são **mascarados** no HTML. | Garante que o relatório de auditoria possa ser compartilhado entre equipes sem vazar os dados que estão sendo auditados. |
| **Classificação de Risco** | **Vermelho (Confirmado/Válido):** E-mail, CPF Válido. **Amarelo (Suspeito):** Telefone, Endereço, CPF Suspeito (falha na matemática). | Prioriza a remediação, focando primeiro nos dados com maior certeza de serem PII sensíveis. |

### ⚙️ Uso da Ferramenta

O scanner é executado via linha de comando (CLI), apontando para a URL alvo e, opcionalmente, o token de autenticação:

```bash
# Exemplo de uso em API protegida:
python pii_scanner.py https://api.exemplo.com/v1/usuarios/ --token SEU_TOKEN_AQUI

# Exemplo de uso em ambiente de testes:
python pii_scanner.py http://127.0.0.1:8000/api/dados_publicos/
```

### 🔑 Lição de DevSecOps

O `PII Scanner` é um exemplo de como é possível **automatizar os requisitos de conformidade**. Em vez de depender apenas de revisões manuais, uma ferramenta pode ser integrada ao CI/CD para bloquear *deployments* se um novo *endpoint* começar a expor PII inesperadamente. Isso reforça a filosofia de *Security by Design* e *Compliance as Code*.
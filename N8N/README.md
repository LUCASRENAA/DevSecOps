# 🛡️ DevSecOps Hub: Automações de Segurança com n8n e Gemini

Este repositório centraliza dois workflows essenciais construídos no **n8n** para incorporar a segurança desde as fases iniciais do desenvolvimento (**Shift Left**). Ambos os fluxos utilizam o Google Gemini para análise de segurança e fornecimento de relatórios técnicos.

-----

## 🚀 Workflows de Segurança em Destaque

Abaixo estão os dois workflows de automação DevSecOps disponíveis neste repositório. Clique nos links para ver a documentação detalhada (`READMEs`) sobre como cada fluxo funciona, quais são seus gatilhos e como são configurados.

| \# | Nome do Arquivo | Objetivo Principal | Tipo de Análise | 🔗 Documentação Detalhada |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `Detector de Injeção N8N.json` | Análise de Código Estática (SAST) em busca de vulnerabilidades de **Injection** (OWASP A03). | Código (Snippet) | [Ver README: Detector de Injeção](https://www.google.com/search?q=%231-detector-de-inje%C3%A7%C3%A3o-n8n-sast-leve) |
| **2** | `Auditoria de Headers de Segurança Web com IA e Relatório por Email.json` | Auditoria dinâmica para verificar a postura de segurança do servidor, analisando **Cabeçalhos HTTP** críticos. | Servidor (DAST Ligeiro) | [Ver README: Auditoria de HTTP Headers](https://www.google.com/search?q=%232-auditoria-web-an%C3%A1lise-de-http-headers) |

-----

-----

## 1\. 💡 Detector de Injeção N8N (SAST Leve)

### Objetivo

Simular um teste de segurança estático (SAST) leve, ideal para ser usado antes de um *commit* ou durante uma revisão de código rápida, focando na detecção de falhas de injeção.

### Como Funciona (Visão Geral)

1.  **Gatilho:** O desenvolvedor insere um snippet de código em um **Formulário Web**.
2.  **Análise:** O nó **`Analisador Regex`** utiliza expressões regulares para detectar padrões clássicos de vulnerabilidades (SQL Injection e Command Injection).
3.  **Fluxo Condicional:** O nó **`Achou Vulnerabilidade?`** direciona o fluxo, garantindo que a resposta (Relatório) seja adequada:
      * **✅ Vulnerabilidade:** Gera **Relatório de Vulnerabilidade** (OWASP com trecho vulnerável).
      * **❌ Limpo:** Gera **Relatório de Análise Segura** (Parabenizando o código).
4.  **Relatório AI (Gemini):** O **Google Gemini** é usado como especialista em AppSec para formatar o resultado de forma técnica e acionável, seguindo o **OWASP Top 10**.
5.  **Entrega:** O resultado é convertido para um arquivo Markdown (`Relatorio-OWASP.md`).

### Parâmetros de Entrada (Formulário)

| Campo | Descrição |
| :--- | :--- |
| **Insira aqui** | O snippet de código (em qualquer linguagem) a ser verificado. |

-----

## 2\. 🌐 Auditoria Web: Análise de HTTP Headers

### Objetivo

Auditar a configuração de segurança do servidor de uma aplicação em *runtime* (em produção ou homologação), focando nos cabeçalhos HTTP que previnem ataques baseados no navegador (XSS, Clickjacking, etc.).

### Como Funciona (Visão Geral)

1.  **Gatilho:** O usuário insere a **URL** do site e o **e-mail** para receber o relatório em um **Formulário Web**.
2.  **Requisição:** O nó **`HTTP Request`** captura os cabeçalhos de resposta do servidor da URL fornecida.
3.  **Processamento:** O nó **`Code in JavaScript`** isola os cabeçalhos de segurança críticos (`Content-Security-Policy`, `X-Frame-Options`, `Strict-Transport-Security`, etc.) e informa seu status (Presente/Ausente).
4.  **Análise AI (Gemini):** O nó **`AI Agent`** usa a inteligência do Google Gemini para analisar os dados brutos e gerar:
      * Uma nota de segurança (0 a 10).
      * Um relatório de impacto dos cabeçalhos ausentes.
      * Recomendações de correção.
5.  **Entrega:** O relatório final é enviado por e-mail para o endereço fornecido no formulário.

### Parâmetros de Entrada (Formulário)

| Campo | Descrição |
| :--- | :--- |
| **Insira o Link a ser analisado** | A URL completa (ex: `https://seu-site.com.br`) do endpoint a ser auditado. |
| **Qual e-mail você quer receber a análise?** | O endereço de e-mail para o qual o relatório será enviado. |

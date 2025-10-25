# Aula 01 — Introdução ao DevSecOps e Pipeline de Segurança
Esta aula introduz DevSecOps e descreve uma pipeline CI/CD (GitHub Actions) que integra varreduras de segurança (SCA, SAST, DAST) e uma etapa de análise de resultados com IA generativa (TinyLlama via Ollama).

## Metodologia — OWASP Web Security Testing Guide (WSTG)
A metodologia adotada nesta disciplina segue os princípios e boas práticas do OWASP WSTG, alinhando avaliações e testes a um padrão reconhecido internacionalmente.  
- Objetivo: estruturar testes de segurança para aplicações web cobrindo todo o fluxo (reconhecimento, autenticação, gestão de sessão, autorização, validação de entrada, armazenamento seguro, configuração segura, etc.).  
- Como usamos no curso: mapear áreas do WSTG para etapas da pipeline — SCA/SAST para análise de dependências e código, DAST para testes dinâmicos em runtime, Modelagem de Ameaças para identificação proativa de vetores conforme WSTG.  
- Resultado esperado: cobertura sistemática das principais superfícies de ataque e priorização de remediações baseada em evidências.

## Objetivos
- Entender o conceito de "Shift Left" em segurança.
- Ver demonstrado um pipeline que automatiza varreduras e envia resultados ao GitHub Security (SARIF).
- Ver um exemplo de uso de IA local para sumarização e priorização de resultados de segurança.

## Principais conceitos
- DevSecOps: integrar segurança desde as fases iniciais do SDLC.
- Benefícios: detecção precoce, redução de custos e software mais resiliente.

## Tipos de análise na pipeline
- Modelagem de Ameaças (TM): identificação proativa de vetores de ataque.
- Análise de Composição de Software (SCA): descoberta de dependências e CVEs (ex.: Trivy).
- Teste de Segurança Estático (SAST): análise de código sem execução (ex.: Bandit para Python).
- Teste de Segurança Dinâmico (DAST): varredura contra a aplicação em execução (ex.: OWASP ZAP).

## Visão geral da pipeline (GitHub Actions)
- Gatilhos: push e pull_request nas branches `main` e `Dev`.
- Permissões: publica SARIF/resultado de segurança (security-events: write).
- Jobs principais:
  - Trivy (SCA / SAST leve) — varre filesystem e gera SARIF.
  - Bandit (SAST para Python) — gera JSON convertido para SARIF via script `bandit_to_sarif.py`.
  - OWASP ZAP (DAST) — inicia servidor (Django) e executa varredura em `http://127.0.0.1:8000`.

## Etapa de IA — TinyLlama via Ollama (opcional/inovadora)
- Objetivo: resumir, priorizar e sugerir mitigações a partir dos SARIF.
- Procedimento resumido:
  1. Instalar Docker/Docker Compose e subir o serviço Ollama.
  2. Baixar o modelo TinyLlama localmente (via Ollama).
  3. Concatenar resultados SARIF (ex.: `trivy-results.sarif`, `bandit-results.sarif`) em um prompt.
  4. Chamar a API local do Ollama (`http://localhost:11399/api/generate`) com o prompt.
  5. Capturar e exibir o resumo/recomendações no log do workflow.

Aviso: usar IA para priorização é auxiliar — confirme sempre com análise humana antes de aplicar mudanças em produção.

## Arquivos relacionados / utilitários
- `bandit_to_sarif.py` — conversor de Bandit JSON para SARIF.
- Workflows: `.github/workflows/security.yml` (exemplo de pipeline que integra as etapas acima).

## Boas práticas rápidas
- Integre varreduras no PR para feedback rápido.
- Publicar SARIF para aproveitar interfaces do GitHub Security.
- Automatize triagem inicial, mas mantenha validação humana para correções críticas.

## Referências rápidas
- Trivy — https://github.com/aquasecurity/trivy
- Bandit — https://github.com/PyCQA/bandit
- OWASP ZAP — https://www.zaproxy.org
- Ollama / TinyLlama — documentação do projeto Ollama

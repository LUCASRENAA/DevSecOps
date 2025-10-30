# 🛡️ Repositório Central: Segurança e Desenvolvimento Mobile

Este repositório serve como um hub central para o desenvolvimento e a garantia de segurança de nossa aplicação mobile. Ele é estruturado em duas áreas principais: o código-fonte da aplicação Android com sua pipeline de segurança configurada, e a documentação detalhada de testes de invasão (Pentest) para mobile.

## 📁 Estrutura do Repositório

| Diretório | Descrição | Status/Foco Principal |
| :--- | :--- | :--- |
| `pipeline_security/` | Contém o **código-fonte** da aplicação Android, seguindo o padrão MVVM, e a **configuração completa da Pipeline de CI/CD** com foco em segurança (DevSecOps). | **Desenvolvimento e DevSecOps** |
| `pentest_mobile/` | Contém a **documentação, relatórios e evidências (imagens)** dos testes de segurança (Pentest) realizados na aplicação mobile. | **Análise de Segurança e Vulnerabilidades** |
| `README.md` (Atual) | Guia central e overview do repositório. | **Navegação e Contexto** |

## 1. 🚀 Código e Pipeline de Segurança (`pipeline_security`)

O diretório `pipeline_security` abriga o projeto Android e a definição de nossa estratégia de **DevSecOps** (Desenvolvimento, Segurança e Operações). A prioridade aqui é integrar verificações de segurança *diretamente* no fluxo de desenvolvimento.

### Foco em Segurança

* **Workflow Dedicado:** O arquivo `.github/workflows/security.yml` indica a presença de uma rotina automatizada de segurança (provavelmente SAST, SCA e/ou análise de segredos) que é executada em cada commit/PR.
* **Ofuscação:** O arquivo `app/proguard-rules.pro` assegura que o código seja ofuscado no build de release, dificultando a engenharia reversa.

### Documentação Detalhada

Para uma visão completa da arquitetura do aplicativo, da estrutura de testes e das boas práticas de segurança implementadas na pipeline de CI/CD, consulte o `README.md` específico:

➡️ **[Clique aqui para ver o README de Pipeline Security](./pipeline_security/README.md)**

## 2. 🕵️‍♂️ Pentest Mobile (`pentest_mobile`)

O diretório `pentest_mobile` armazena toda a documentação gerada a partir dos testes de invasão e análise de vulnerabilidades realizados em nossa aplicação.

### Conteúdo Principal

* **Relatórios e Análise:** O `README.md` interno deve detalhar a metodologia, o escopo e os principais achados do Pentest.
* **Evidências:** A pasta `imgs/` (com arquivos como `1.png`, `2.png`, `certificado-pentest-android.png`) contém *screenshots* e provas concretas das vulnerabilidades encontradas e exploradas, servindo como base para a correção (remediação).

### Documentação Detalhada

Para acessar os relatórios e evidências do Pentest, incluindo detalhes sobre as vulnerabilidades e recomendações, consulte o `README.md` específico:

➡️ **[Clique aqui para ver o README de Pentest Mobile](./pentest_mobile/README.md)**
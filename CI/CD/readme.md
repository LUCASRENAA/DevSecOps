Quarto (e último) README para documentar a aula sobre **CI/CD (Integração Contínua e Entrega Contínua)**, focando em sua importância no contexto DevSecOps e na anatomia do *workflow* demonstrado.

## 📝 Aula 07: O Coração do DevSecOps – Integração e Entrega Contínua (CI/CD)

Esta aula finalizou o conteúdo técnico, abordando o **CI/CD (Continuous Integration/Continuous Delivery)** como a espinha dorsal da metodologia DevSecOps. A pipeline de segurança demonstrada foi desconstruída para explicar como a automação de testes e segurança se encaixa no processo de desenvolvimento.

---

## 🔁 O que é CI/CD?

CI/CD é um conjunto de práticas que permite que as equipes de desenvolvimento entreguem alterações de código com mais frequência e confiança, automatizando as etapas de *build*, teste e *deployment*.

### 1. Integração Contínua (CI - Continuous Integration)

* **O que é:** Uma prática de desenvolvimento onde os desenvolvedores mesclam suas alterações de código na *branch* principal de um repositório (ex: `main`) várias vezes ao dia.
* **Propósito:** Evitar problemas de integração tardia. Cada mesclagem dispara uma série de testes automatizados (*unit tests*, SAST, SCA) para verificar se o código não quebrou nada.
* **No DevSecOps:** É aqui que as ferramentas de segurança (Bandit, Trivy) são executadas para fornecer *feedback* imediato sobre novas vulnerabilidades introduzidas.

### 2. Entrega Contínua (CD - Continuous Delivery)

* **O que é:** Uma extensão do CI que garante que o código, após passar por todos os testes automatizados, está sempre em um estado pronto para ser liberado para produção (Deployment).
* **Propósito:** Reduzir o tempo e o risco do processo de *release*.
* **No DevSecOps:** A pipeline CD automatiza a construção do artefato (ex: imagem Docker) e, frequentemente, inclui o DAST (como o ZAP) antes que o artefato seja promovido.

---

## 🔩 Anatomia de uma Pipeline (GitHub Actions)

O *workflow* `Security Scan` é um exemplo prático de uma pipeline de CI/CD focada em segurança.

### Terminologia de Pipelines

| Termo | O que é? | Exemplo no Workflow |
| :--- | :--- | :--- |
| **Workflow** | O arquivo YAML que define todo o processo automatizado. | O arquivo completo `Security Scan`. |
| **Gatilho (`on`)** | O evento que inicia o *workflow*. | `on: push` (Toda vez que há um *push* de código). |
| **Job** | Um conjunto de passos que é executado em um **Runner**. Os *Jobs* geralmente são executados em paralelo. | `jobs: security` |
| **Runner** | A máquina virtual (VM) ou contêiner onde o *Job* é executado. | `runs-on: ubuntu-latest` (Uma VM Linux padrão). |
| **Step** | Uma tarefa individual que um *Job* executa (ex: rodar um comando, executar um *script*). | `- name: Checkout repository` |
| **Action (`uses`)** | Um bloco de código reutilizável que encapsula uma tarefa complexa (ex: `actions/checkout@v3`). | `- uses: aquasecurity/trivy-action@0.20.0` |

---

## 🛡️ Análise do Workflow `Security Scan`

Esta pipeline integra as três principais categorias de varredura de segurança em um único *job* automatizado:

### 1. Preparação e Configuração

* **Gatilho:** `push` em qualquer *branch* (`'*'`). Isso garante que a segurança seja verificada em todas as linhas de desenvolvimento.
* **Permissões:** A permissão `security-events: write` é vital, permitindo que os resultados SARIF (gerados pelo Trivy e Bandit) sejam enviados e visualizados na aba **Security** do GitHub.
* **Setup:** Ações para fazer *checkout* do código e configurar o ambiente Python (necessário para Bandit e Django).

### 2. SCA e SAST (Análise Estática)

| Ferramenta | Tipo de Análise | Objetivo no CI |
| :--- | :--- | :--- |
| **Trivy** | **SCA** (Software Composition Analysis) | Varre dependências e sistema de arquivos (`scan-type: 'fs'`) em busca de vulnerabilidades (CVEs). Os resultados são gerados em formato SARIF. |
| **Bandit** | **SAST** (Static Analysis Security Testing) | Varre o código Python em busca de falhas de codificação insegura. Os resultados são convertidos de JSON para SARIF para serem aceitos pelo GitHub. |
| **`github/codeql-action/upload-sarif@v3`** | **Integração** | Ação crucial que permite que o GitHub Security visualize e alerte sobre as descobertas do Trivy e Bandit. |

### 3. DAST (Análise Dinâmica)

A fase DAST exige que a aplicação esteja em um estado **executável**, simulando um ambiente real.

* **Setup do Servidor:**
    * O comando `python manage.py migrate` prepara o banco de dados.
    * `python manage.py runserver &` inicia o servidor Django em segundo plano (o `&` é crucial para que o *workflow* possa continuar a executar os próximos passos).
    * A **Chave Secreta** (`SECRET_KEY`) é injetada de forma segura usando **GitHub Secrets** (`${{ secrets.DJANGO_PROD_SECRET_KEY }}`).
* **OWASP ZAP Baseline Scan:**
    * O *Action* do ZAP é executado, apontando para o servidor local (`target: "http://127.0.0.1:8000"`).
    * Faz uma varredura dinâmica leve e gera um relatório SARIF (`sarif_output: zaproxy.sarif`).
* **Limpeza:** O `pkill -f "python manage.py runserver"` é essencial para **encerrar o processo do servidor** após o *scan*, liberando recursos da VM e garantindo que o *job* finalize corretamente.
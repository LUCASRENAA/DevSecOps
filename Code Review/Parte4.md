## 📝 Aula 04: Fundamentos de Django e Controle de Versão com Git

Esta aula marcou o início da exploração de um *framework* web moderno – **Django** – e reforçou os conceitos essenciais de **Controle de Versão** com **Git**, uma habilidade fundamental para a colaboração e a integração de segurança.

---

## 💻 Introdução ao Framework Web Django

Django é um *framework* de desenvolvimento web de código aberto, escrito em Python, conhecido por sua filosofia "Baterias Incluídas" (*Batteries Included*), visando a produtividade e a segurança.

### 🌐 Princípios do Django

* **Python-based:** Utiliza a sintaxe limpa e poderosa do Python.
* **Completo:** Oferece ferramentas prontas para ORM (Mapeamento Objeto-Relacional), rotas, *templates*, sistema de autenticação, e um painel administrativo.
* **Design MTV (Model-Template-View):** Semelhante ao padrão MVC (Model-View-Controller), mas com uma nomenclatura ajustada ao ambiente web:
    * **Model:** Define a estrutura dos dados (interage com o banco de dados).
    * **Template:** Define a interface do usuário (o que o usuário vê).
    * **View:** É a lógica de negócios que processa a requisição, interage com o **Model** e decide qual **Template** renderizar.
* **Segurança:** Django é projetado para ajudar a evitar muitas vulnerabilidades comuns (como XSS, CSRF, SQL Injection) por padrão, o que é um grande ponto a favor no contexto DevSecOps.

### Estrutura Básica de um Projeto Django

Um projeto Django é tipicamente organizado em:

| Componente | Função |
| :--- | :--- |
| **Projeto** | O contêiner de configuração de todo o projeto (arquivos `settings.py`, `urls.py`). |
| **App** | Um módulo independente que lida com uma função específica (ex: usuários, blog, *e-commerce*). |
| **`settings.py`** | Configurações globais (banco de dados, segurança, *apps* instalados). |
| **`urls.py`** | O roteador principal, que mapeia URLs para as funções de *View*. |
| **`manage.py`** | Utilitário de linha de comando para tarefas administrativas (migrações, execução do servidor, etc.). |

---

## 🌳 Controle de Versão com Git

Git é o sistema de controle de versão distribuído mais utilizado no mundo, essencial para gerenciar o código-fonte de forma colaborativa e segura.

### 1. Conceitos Fundamentais

| Conceito | Descrição |
| :--- | :--- |
| **Repositório (`Repo`)** | O diretório que contém todos os arquivos do projeto, junto com o histórico de todas as alterações (`.git`). |
| **Commit** | Um "instantâneo" (snapshot) do projeto em um determinado momento, com uma mensagem descritiva. Representa uma unidade de mudança. |
| **Branch** | Uma linha de desenvolvimento paralela e independente. Permite que equipes trabalhem em novos recursos ou correções sem afetar a linha principal (ex: `main` ou `dev`). |
| **Merge / Rebase** | Processos para integrar as mudanças de uma *branch* em outra. |
| **HEAD** | O ponteiro que aponta para o *commit* atual (tipicamente o último *commit* da *branch* em que você está). |

### 2. Fluxo de Trabalho Básico (Três Árvores do Git)

O Git gerencia o projeto em três estados principais:

1.  **Working Directory (Diretório de Trabalho):** Os arquivos que você está editando no momento.
2.  **Staging Area (Área de Preparação):** Onde você marca as alterações que deseja incluir no próximo *commit* (`git add`).
3.  **Repository (Repositório Local):** O histórico permanente das alterações (onde os *commits* são armazenados).

### 3. Comandos Essenciais

| Comando | Função |
| :--- | :--- |
| `git clone [url]` | Baixa um repositório remoto para a máquina local. |
| `git status` | Exibe o estado dos arquivos no diretório de trabalho e *staging area*. |
| `git add [arquivo]` | Move as alterações do *Working Directory* para o *Staging Area*. |
| `git commit -m "[mensagem]"` | Cria um *commit* permanente com as alterações do *Staging Area*. |
| `git push` | Envia os *commits* locais para o repositório remoto (GitHub/GitLab/Bitbucket). |
| `git pull` | Puxa as alterações do repositório remoto e as integra ao repositório local. |
| **`git stash`** | **Salva temporariamente as alterações locais sem comitar**, permitindo a troca de *branches* (como visto na Aula 3). |
| `git branch [nome]` | Cria uma nova *branch*. |
| `git checkout [nome]` | Troca para uma *branch* existente. |

### 🔒 Git e DevSecOps

O uso rigoroso do Git é fundamental para o DevSecOps:

* **Auditabilidade:** Todo *commit* é rastreável (quem fez, quando fez, o que mudou), crucial para auditorias de segurança.
* **Triggers CI/CD:** O Git (e plataformas como o GitHub) é o gatilho para a execução das pipelines de segurança (como a `Full Security Scan` da Aula 01).
* **Branch Protection:** Permite impor regras de segurança, como exigir que todas as mudanças passem por varreduras SAST/SCA e Code Reviews antes de serem integradas à *branch* principal.
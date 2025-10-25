## 📝 Aula 03: Code Review, Ferramentas SCA/SAST e Prevenção de Injeção de Comandos

Esta aula abordou o **Code Review** como uma prática essencial de DevSecOps, focando tanto na análise manual (com checklists) quanto na utilização de ferramentas automatizadas como **Trivy (SCA)** e **Bandit (SAST)**. A parte prática exemplificou o risco crítico da Injeção de Comandos.

---

## 🧐 Revisão de Código Focada em Segurança (Security Code Review)

O Code Review é um momento ideal para "caçar" vulnerabilidades que as ferramentas automatizadas podem ter perdido, garantindo que o código siga as melhores práticas de segurança desde a sua concepção.

### ❓ Checklist de Segurança para Code Review

Ao revisar o código, o analista deve se fazer perguntas críticas, alinhadas com os princípios de desenvolvimento seguro:

* **Quais são os tipos de dados?**
    * *Confirmação:* Os tipos de dados esperados (string, inteiro, booleano, etc.) estão sendo validados corretamente? A ausência de validação de tipo pode levar a erros inesperados e falhas de segurança.
* **Todos os dados do usuário estão sendo tratados (sanitizados)?**
    * *Mitigação:* A entrada do usuário é a principal porta de entrada para ataques. Todo dado vindo de fontes externas (usuário, arquivos, APIs, etc.) deve ser **sanitizado** (limpo para remover conteúdo malicioso) e/ou **validado** (para garantir que corresponda ao formato esperado).
* **As senhas estão em texto claro?**
    * *Proteção:* Senhas e outros segredos nunca devem ser armazenados em texto claro (plain text). É obrigatório o uso de funções *hashing* seguras e lentas (como Argon2, bcrypt ou scrypt) com *salt* adequados.
* **As funções estão muito complexas?**
    * *Manutenibilidade e Segurança:* Funções excessivamente longas ou complexas (*high complexity*) são difíceis de entender, manter e, principalmente, de auditar em busca de *bugs* ou falhas de segurança.

---

## 🛠️ Ferramentas Automatizadas de Segurança

A revisão manual de código deve ser complementada por ferramentas que escalam a análise em grandes bases de código, integradas diretamente à pipeline CI/CD (como visto na Aula 01).

### 1. SCA (Software Composition Analysis) - Exemplo: Trivy

* **Foco:** **Código de Terceiros** (bibliotecas, dependências, imagens Docker).
* **O que faz:** Varre o arquivo de dependências (`requirements.txt`, `package.json`, etc.) para identificar vulnerabilidades conhecidas (CVEs) em componentes *open source* utilizados pelo projeto.
* **Exemplo Prático (Trivy):**
    * Analisa o ambiente (sistema de arquivos ou imagem Docker) e lista bibliotecas com falhas de segurança críticas ou de alta severidade, permitindo que o desenvolvedor as atualize ou as substitua.

### 2. SAST (Static Application Security Testing) - Exemplo: Bandit

* **Foco:** **Código Próprio** (código-fonte escrito pela equipe).
* **O que faz:** Analisa o código estaticamente (sem executá-lo) em busca de padrões de codificação inseguros que possam levar a vulnerabilidades (ex: senhas *hardcoded*, uso inseguro de `os.system`, falhas de criptografia).
* **Exemplo Prático (Bandit):**
    * Ferramenta focada em código Python que detecta automaticamente o uso inseguro de funções, como a execução de comandos do sistema com entradas não sanitizadas (o alvo da demonstração prática abaixo).

---

## 🔒 Segurança em Ação: Prevenção de Injeção de Comandos

A injeção de comandos é uma vulnerabilidade grave que ocorre quando um atacante consegue executar comandos arbitrários no servidor do sistema operacional através de uma entrada não validada na aplicação.

### Cenário de Vulnerabilidade em Python

A vulnerabilidade principal explorada foi o uso da função `os.system()` ou similares (como `subprocess.call` com `shell=True`) com dados de usuário não tratados.

#### Script 1: ❌ Inseguro

* **Vulnerabilidade:** O comando é construído diretamente com a entrada do usuário (`f"ping {ip}"`) e executado por `os.system()`, que invoca um *shell* do sistema operacional. O uso do ponto-e-vírgula (`;`) ou *pipes* (`|`) permite que o atacante "escape" do comando `ping` e execute comandos subsequentes (ex: `ls -la`).
* **Resultado do Bandit (SAST):** Ferramentas como o Bandit alertariam para o uso da função `os.system` com variáveis de usuário não sanitizadas.

#### Script 2: ✅ Validação Manual (Melhoria)

* **Mitigação:** Implementa uma função de validação (`is_valid_ipv4`) para garantir que a entrada corresponda exatamente ao formato esperado (neste caso, um IPv4).
* **Princípio:** Garante que apenas dados com **formato conhecido e seguro** cheguem ao comando do sistema operacional, bloqueando caracteres perigosos como `;`, `|`, `$()`, etc.

#### Script 3: ✨ Validação com Biblioteca (Melhor Prática)

* **Melhor Prática:** Utiliza uma biblioteca padrão e robusta (`ipaddress`) para a validação.
* **Benefício:** Bibliotecas dedicadas fornecem validação mais completa e menos propensa a erros do que a lógica manual, pois tratam de *edge cases* (casos de limite) e formatos complexos. O uso de `try...except` lida elegantemente com entradas inválidas.

### **Conclusão:**

A melhor defesa contra injeções é **nunca confiar em entradas externas**. Sempre **valide** e/ou **sanitize** rigorosamente todos os dados de usuário antes de usá-los em comandos do sistema, *queries* de banco de dados (SQL Injection), ou qualquer contexto que interaja com o sistema operacional ou infraestrutura.
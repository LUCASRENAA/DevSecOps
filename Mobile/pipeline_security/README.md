# 📱 Projeto: Template de Aplicação Android (MVVM + Navigation)

## 🌟 Visão Geral do Projeto

Este projeto serve como um **template (modelo) base** para o desenvolvimento de aplicações Android, utilizando uma arquitetura robusta e moderna. Ele demonstra a implementação de um aplicativo com navegação por abas inferiores (`BottomNavigationView`), seguindo o padrão arquitetural **MVVM (Model-View-ViewModel)** com a utilização dos componentes **Android Jetpack** (como **LiveData**, **ViewModel** e **Navigation Components**).

O objetivo principal é fornecer uma base limpa, testável e escalável, que já incorpora as melhores práticas de desenvolvimento e uma pipeline de CI/CD pensada em segurança.

## 🏗 Estrutura do Projeto

O projeto segue a estrutura padrão de um aplicativo Android, organizado pelo padrão de pacote de recurso:

```
└── ./
    └── app
        └── src
            ├── androidTest  // Testes de Instrumentação (em dispositivos/emuladores)
            ├── main         // Código principal da aplicação
            │   └── java
            │       └── com.example.aaaaaaa
            │           ├── ui              // Pacotes para Fragments e ViewModels
            │           │   ├── dashboard
            │           │   ├── home
            │           │   └── notifications
            │           └── MainActivity.java // Atividade principal
            └── test         // Testes de Unidade (em máquina local/JVM)
```

## ⚙️ Pipeline de CI/CD (Integração e Entrega Contínuas)

A pipeline de CI/CD é fundamental para garantir a qualidade, estabilidade e segurança do código que chega à produção. Embora as etapas exatas possam depender da ferramenta (e.g., GitHub Actions, GitLab CI, Jenkins), a filosofia de segurança deve ser a seguinte:

| Etapa | Objetivo | Boas Práticas de Segurança Aplicadas |
| :--- | :--- | :--- |
| **1. Build e Testes** | Compilar o código e executar testes automatizados. | **Testes de Unidade e Instrumentação:** Garante que a lógica do aplicativo funcione conforme o esperado e evita regressões. |
| **2. Análise Estática de Código (SAST)** | Analisar o código-fonte sem executá-lo para encontrar vulnerabilidades. | **Scanning de Código:** Utilização de ferramentas como **SonarQube**, **SpotBugs** ou **CodeQL** para verificar falhas comuns de segurança (e.g., injeção de SQL, hardcode de credenciais). |
| **3. Análise de Dependências (SCA)** | Verificar vulnerabilidades em bibliotecas de terceiros (dependências). | **Scanning de Dependências:** Uso de ferramentas como **OWASP Dependency-Check** para identificar e alertar sobre bibliotecas com CVEs (Vulnerabilidades e Exposições Comuns). |
| **4. Assinatura e Segurança do Artefato** | Assinar o APK/AAB e proteger a integridade do pacote. | **Gerenciamento de Chaves:** A chave de assinatura deve ser armazenada em um **cofre de segredos (Secret Vault)** seguro e acessível apenas pela pipeline, nunca no repositório. |
| **5. Deploy (Entrega)** | Distribuir o aplicativo para canais de teste (Alpha/Beta) ou para a loja (Google Play). | **Revisão e Aprovação:** Etapa manual ou automática que exige aprovação antes de um *release* de produção. |

## 🔒 Boas Práticas de Segurança em Destaque

A segurança é prioridade desde o *design* (Security-by-Design). As seguintes práticas são obrigatórias neste projeto:

### 1\. Gerenciamento de Segredos (Secrets)

  * **NUNCA** faça *hardcode* de chaves de API, tokens de acesso ou credenciais diretamente no código-fonte ou em arquivos de configuração que são versionados (ex: `strings.xml`, `build.gradle`).
  * Utilize o **Secrets Gradle Plugin** ou armazene chaves em arquivos não versionados ou em **variáveis de ambiente** acessíveis apenas na pipeline de build.

### 2\. Armazenamento de Dados

  * **Evitar** usar `SharedPreferences` para dados sensíveis. Prefira o **EncryptedSharedPreferences** (do Android Jetpack Security Library) ou o **Keystore da Android** para dados críticos, garantindo que o armazenamento local seja criptografado.

### 3\. Comunicação de Rede

  * **Forçar HTTPS:** Garantir que todas as conexões com o backend utilizem o protocolo **TLS/SSL (HTTPS)**. Utilize a funcionalidade **Network Security Configuration** do Android para garantir que apenas conexões seguras sejam permitidas.

### 4\. Proteção de Componentes (Exportação)

  * **Limitar a Exposição:** Revise o arquivo `AndroidManifest.xml` para garantir que apenas componentes necessários (Activities, Services, Broadcast Receivers) sejam marcados com `android:exported="true"`. A exportação desnecessária pode permitir que aplicativos maliciosos interajam com o seu.

### 5\. Obfuscation e Minification

  * Utilizar **R8/ProGuard** no build de *release* para ofuscar o código e dificultar a **engenharia reversa**, protegendo a propriedade intelectual e a lógica interna do aplicativo.


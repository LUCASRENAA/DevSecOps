## Segurança: Prevenção de Injeção de Comandos

Ao receber entradas de usuários, é essencial validar e sanitizar os dados para evitar ataques de injeção de comandos. Veja abaixo exemplos práticos em Python:

---

### Script 1: **Inseguro**
Este script é vulnerável porque executa diretamente o que o usuário digita:
```python
import os

ip = input("Digite o IP ou domínio para pingar: ")
command = f"ping {ip}"
os.system(command)
```
> **Risco:** Um atacante pode digitar `8.8.8.8; ls -la` e executar comandos maliciosos.

**Como testar:**
- **Teste 1 (entrada normal):** Digite `8.8.8.8`. O script executa o ping normalmente.
- **Teste 2 (ataque):** Digite `8.8.8.8; ls -la`. O script executa o ping e depois o comando `ls -la`, mostrando que a entrada não foi validada.

---

### Script 2: **Validação Manual**
Valida manualmente se a entrada é um IPv4 válido:
```python
import os

def is_valid_ipv4(ip_string):
    parts = ip_string.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        try:
            num = int(part)
            if not (0 <= num <= 255):
                return False
        except ValueError:
            return False
    return True

ip_ou_dominio = input("Digite o IP para pingar: ")

if is_valid_ipv4(ip_ou_dominio):
    print(f"\nO endereço '{ip_ou_dominio}' é um IP válido. Ping executado.")
    command = f"ping {ip_ou_dominio}"
    os.system(command)
else:
    print(f"\nO endereço '{ip_ou_dominio}' não é um IP")
```
**Como testar:**
- **Teste 1 (entrada normal):** Digite `8.8.8.8`. O script reconhece como IP válido e executa o ping.
- **Teste 2 (entrada inválida):** Digite `8.8.8`. O script informa que não é um IP válido.
- **Teste 3 (ataque):** Digite `8.8.8.8; ls -la`. O script bloqueia a entrada e não executa comandos maliciosos.

---

### Script 3: **Validação com Biblioteca**
Utiliza a biblioteca padrão `ipaddress` para validação robusta:
```python
import os
import ipaddress

ip_ou_dominio = input("Digite o IP para pingar: ")

try:
    ipaddress.ip_address(ip_ou_dominio)
    command = f"ping {ip_ou_dominio}"
    os.system(command)
except ValueError:
    print(f"\nO endereço '{ip_ou_dominio}' não é um IP.")
```
**Como testar:**
- **Teste 1 (entrada normal):** Digite `8.8.8.8`. O script reconhece como IP válido e executa o ping.
- **Teste 2 (entrada inválida):** Digite `exemplo.com`. O script informa que não é um IP válido.
- **Teste 3 (ataque):** Digite `8.8.8.8; ls -la`. O script detecta a entrada inválida e não executa comandos, garantindo segurança.

---

> **Dica:** Sempre utilize validação adequada para proteger seu sistema contra
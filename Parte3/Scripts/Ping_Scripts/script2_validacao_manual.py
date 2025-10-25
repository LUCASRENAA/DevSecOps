
 
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
 
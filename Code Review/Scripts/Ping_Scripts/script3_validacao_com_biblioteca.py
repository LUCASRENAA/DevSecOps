import os
import ipaddress
 
 
ip_ou_dominio = input("Digite o IP para pingar: ")
 
try:
    ipaddress.ip_address(ip_ou_dominio)
    command = f"ping {ip_ou_dominio}"
    os.system(command)
except ValueError:
    print(f"\nO endereço '{ip_ou_dominio}' não é um IP.")

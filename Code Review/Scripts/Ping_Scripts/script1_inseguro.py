import os
 
ip = input("Digite o IP ou domínio para pingar: ")
command = f"ping {ip}"
os.system(command)
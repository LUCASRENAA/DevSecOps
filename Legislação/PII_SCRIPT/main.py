import requests
import re
import json
import argparse
import datetime
import os # Importação da biblioteca OS
from typing import Union, List, Dict, Any, Tuple

# --- Padrões de Expressão Regular (Regex) ---
CPF_PATTERN = re.compile(r'(\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{11})')
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
PHONE_PATTERN = re.compile(r'(\(?\d{2}\)?\s?|\d{2}\s?)\d{4,5}[-\s]?\d{4}')
ADDRESS_KEYWORDS = r'(rua|av\s?|avenida|travessa|alameda|praça|beco|loteamento|nº|numero|número|apto|apartamento|cep|q\s?|quadra)'
ADDRESS_PATTERN = re.compile(r'(' + ADDRESS_KEYWORDS + r'[.\s]*\s?[-]*\d{1,5}|\d{1,5}\s*[-]*[.\s]*' + ADDRESS_KEYWORDS + r')', re.IGNORECASE | re.DOTALL)

# --- Variáveis Globais para Coleta de Resultados ---
PII_RESULTS = {
    'validos': [],
    'suspeitos': [],
    'total_pontos_checados': 0
}

# --- Funções de Validação e Mascaramento ---

def remove_cpf_formatting(cpf: str) -> str:
    """Remove pontos e traços do CPF."""
    return re.sub(r'[\.\-]', '', cpf)

def validate_cpf_math(cpf_number: str) -> bool:
    """Realiza a validação matemática do CPF."""
    cpf = remove_cpf_formatting(cpf_number)
    
    if not cpf or len(cpf) != 11 or len(set(cpf)) == 1:
        return False

    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    if int(cpf[9]) != digito1:
        return False

    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    if int(cpf[10]) != digito2:
        return False
        
    return True

def mask_pii_value(detail: str, original_value: str) -> str:
    """Mascarar o valor do PII com base no tipo."""
    
    # 1. Mascaramento de CPF / Telefone
    if "CPF" in detail or "Telefone" in detail:
        number = remove_cpf_formatting(original_value)
        if len(number) >= 5:
            # Mantém 3 primeiros e 2 últimos (ex: 123.***.**)
            masked = number[:3] + '***' * (len(number) - 5) + number[-2:]
            return masked
        return "[Mascarado - Numérico]"

    # 2. Mascaramento de E-mail
    elif "Email" in detail:
        try:
            # Precisa usar original_value.split(': ')[-1] se a string ainda contiver o status
            # Mas como estamos passando o valor puro, usamos diretamente:
            user, domain = original_value.split('@')
            # Mantém 3 primeiros do usuário (ex: joa***@exemplo.com)
            masked_user = user[:3] + '***'
            return f"{masked_user}@{domain}"
        except:
            return "[Mascarado - Email]"
            
    # 3. Mascaramento de Endereço Físico e Outros
    elif "Endereço" in detail:
        return "[Endereço Suspeito Mascarado]"

    return "[Mascarado]" # Fallback para qualquer outro PII

# --- Função de Validação Principal ---

def validate_pii(text: str, path: str):
    """
    Verifica se a string contém PII e armazena os resultados na variável global,
    separando o status do valor original.
    """
    global PII_RESULTS
    
    found_pii = []
    valid_cpfs = []

    # 1. Checagem de CPF
    cpf_matches = CPF_PATTERN.findall(text)
    for match in cpf_matches:
        cpf_limpo = remove_cpf_formatting(match)
        
        if len(cpf_limpo) == 11 and cpf_limpo.isdigit():
            status_desc = "CPF suspeito (11 dígitos)"
            tipo = "Suspeito"
            
            if validate_cpf_math(cpf_limpo):
                status_desc = "CPF VÁLIDO (Matemática OK)"
                tipo = "Válido"
                valid_cpfs.append(cpf_limpo)
            
            PII_RESULTS['validos' if tipo == 'Válido' else 'suspeitos'].append({
                'path': path,
                'detalhe_status': status_desc,
                'valor_original': cpf_limpo
            })
            found_pii.append(f"{status_desc}: {match}") 
            
    # 2. Checagem de E-mail (Sempre PII Válido/Confirmado)
    if EMAIL_PATTERN.search(text):
        match = EMAIL_PATTERN.search(text)
        status_desc = "Email encontrado"
        email_value = match.group(0)
        
        PII_RESULTS['validos'].append({
            'path': path,
            'detalhe_status': status_desc,
            'valor_original': email_value
        })
        found_pii.append(f"{status_desc}: {email_value}")
    
    # 3. Checagem de Telefone (Sempre PII Suspeito)
    phone_matches = PHONE_PATTERN.findall(text)
    if phone_matches:
        for match in phone_matches:
            full_match = ''.join(m for m in match if m)
            phone_limpo = remove_cpf_formatting(full_match)
            
            if phone_limpo not in valid_cpfs and len(phone_limpo) in [10, 11]:
                 status_desc = "Telefone suspeito"
                 
                 PII_RESULTS['suspeitos'].append({
                    'path': path,
                    'detalhe_status': status_desc,
                    'valor_original': full_match
                 })
                 found_pii.append(f"{status_desc}: {full_match}")
                 
    # 4. Checagem de Endereço Físico (Sempre PII Suspeito)
    address_matches = ADDRESS_PATTERN.findall(text)
    if len(address_matches) >= 2:
        example_match = ", ".join(m[0] for m in address_matches[:2])
        status_desc = "Endereço Físico suspeito (2+ termos)"

        PII_RESULTS['suspeitos'].append({
            'path': path,
            'detalhe_status': status_desc,
            'valor_original': example_match
        })
        found_pii.append(f"{status_desc}: {example_match}...")

    return found_pii

# --- Funções de API e Scan (Inalteradas) ---

def get_api_data(url: str, headers: Dict[str, str] = None) -> Union[List, Dict, None]:
    """Faz a requisição GET na URL e retorna os dados em formato Python (JSON)."""
    print(f"-> Acessando URL: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERRO ao acessar a URL {url}: {e}")
        return None

def scan_endpoint(data: Union[List, Dict, Any], path: str = ""):
    """Recursivamente varre o JSON para validar PII e armazena."""
    global PII_RESULTS
    
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            scan_endpoint(value, new_path)
            
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_path = f"{path}[{index}]"
            scan_endpoint(item, new_path)
            
    elif isinstance(data, str):
        PII_RESULTS['total_pontos_checados'] += 1
        pii_results = validate_pii(data, path)
        
        # Log no Terminal (versão sem cores)
        if pii_results:
            print(f"\n!!! PII ENCONTRADO !!!")
            print(f"  > Caminho (Path): {path}")
            print(f"  > Valor (Exemplo da String): '{data[:50]}...'") 
            for result in pii_results:
                 print(f"    - {result}")
            print("-------------------------------------")


# --- FUNÇÃO DE GERAÇÃO DE HTML (NOVO OUTPUT DE CAMINHO ABSOLUTO) ---

def generate_html_report(api_url: str):
    """
    Gera o relatório de auditoria em um arquivo HTML e retorna o caminho absoluto.
    """
    validos = PII_RESULTS['validos']
    suspeitos = PII_RESULTS['suspeitos']
    total_validos = len(validos)
    total_suspeitos = len(suspeitos)
    
    data_execucao = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

    # --- Conteúdo da Tabela de Válidos ---
    tabela_validos = ""
    for item in validos:
        valor_mascarado = mask_pii_value(item['detalhe_status'], item['valor_original'])
        tabela_validos += f"""
        <tr class="pii-confirmed">
            <td><code>{item['path']}</code></td>
            <td>{item['detalhe_status']}</td> 
            <td>{valor_mascarado}</td>
        </tr>
        """
    if not tabela_validos:
        tabela_validos = '<tr><td colspan="3">Nenhum PII confirmado/válido encontrado.</td></tr>'

    # --- Conteúdo da Tabela de Suspeitos ---
    tabela_suspeitos = ""
    for item in suspeitos:
        valor_mascarado = mask_pii_value(item['detalhe_status'], item['valor_original'])
        tabela_suspeitos += f"""
        <tr class="pii-suspect">
            <td><code>{item['path']}</code></td>
            <td>{item['detalhe_status']}</td> 
            <td>{valor_mascarado}</td>
        </tr>
        """
    if not tabela_suspeitos:
        tabela_suspeitos = '<tr><td colspan="3">Nenhum PII suspeito encontrado.</td></tr>'


    # --- Template HTML Principal ---
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório de Auditoria PII - {api_url}</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; background-color: #f4f4f9; }}
            .container {{ max-width: 1200px; margin: auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 0 15px rgba(0,0,0,0.1); }}
            h1 {{ color: #1e3a8a; border-bottom: 2px solid #1e3a8a; padding-bottom: 10px; }}
            h2 {{ color: #3b82f6; margin-top: 30px; }}
            .confidential {{ 
                background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; 
                padding: 15px; margin-bottom: 25px; border-radius: 4px; font-weight: bold;
                text-align: center; font-size: 1.1em;
            }}
            .summary-box {{ display: flex; justify-content: space-around; margin: 20px 0; gap: 20px; }}
            .summary-item {{ padding: 20px; border-radius: 6px; flex: 1; text-align: center; font-size: 1.1em; }}
            .valid {{ background-color: #ffe0e0; border: 1px solid #ef4444; color: #7f1d1d; }} /* Alto Risco - Vermelho */
            .suspect {{ background-color: #fef3c7; border: 1px solid #fbbd23; color: #92400e; }} /* Potencial - Amarelo/Laranja */
            .count {{ font-size: 2.5em; font-weight: bold; display: block; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #eff6ff; color: #1e3a8a; }}
            .pii-confirmed td {{ background-color: #ffebeb; font-weight: bold; color: #b91c1c; }} /* Linhas da tabela VERMELHO CLARO */
            .pii-suspect td {{ background-color: #fffbef; }}
            code {{ background-color: #eee; padding: 2px 4px; border-radius: 3px; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="confidential">
                AVISO: DOCUMENTO ESTRITAMENTE CONFIDENCIAL. CONTÉM INFORMAÇÕES SENSÍVEIS SOBRE VAZAMENTO DE PII.
            </div>
            <h1>Relatório de Auditoria de PII da API</h1>
            <p><strong>URL Auditada:</strong> <code>{api_url}</code></p>
            <p><strong>Data de Execução:</strong> {data_execucao}</p>
            <p><strong>Pontos de Texto Checados:</strong> {PII_RESULTS['total_pontos_checados']}</p>

            <h2>Sumário Executivo</h2>
            <p>Este relatório apresenta os achados de Informações de Identificação Pessoal (**PII**) encontrados no endpoint da API auditado. Todos os valores de PII no detalhe foram **mascarados** para evitar risco de exposição no próprio relatório.</p>
            <ul>
                <li><strong>PII Confirmado/Válido (Alto Risco - VERMELHO):</strong> Inclui **E-mail** e **CPF com validação matemática OK**. Estes dados são classificados como PII de forma inequívoca.</li>
                <li><strong>PII Suspeito (Risco Potencial - AMARELO/LARANJA):</strong> Inclui **CPF (11 dígitos, falha na matemática)**, **Telefone** e **Endereço Físico**. A identificação é baseada em padrões de regex.</li>
            </ul>

            <h2>Resumo Estatístico</h2>
            <div class="summary-box">
                <div class="summary-item valid">
                    <span class="count">{total_validos}</span>
                    PII Confirmado / Válido (Alto Risco)
                </div>
                <div class="summary-item suspect">
                    <span class="count">{total_suspeitos}</span>
                    PII Suspeito (Risco Potencial)
                </div>
            </div>

            <h2>Detalhes dos PII Confirmados/Válidos ({total_validos} Achados)</h2>
            <p>Os valores encontrados abaixo foram **mascarados**. O valor completo original deve ser obtido através da checagem do *log* de execução ou da fonte de dados, usando o <strong>Caminho (Path)</strong>.</p>
            <table>
                <thead>
                    <tr>
                        <th>Caminho (Path) no JSON</th>
                        <th>Tipo e Status</th>
                        <th>Valor Mascarado</th>
                    </tr>
                </thead>
                <tbody>
                    {tabela_validos}
                </tbody>
            </table>

            <h2>Detalhes dos PII Suspeitos ({total_suspeitos} Achados)</h2>
            <p>Estes dados foram identificados por padrões (Telefone, Endereço Físico) ou falharam na validação. Os valores também foram **mascarados**.</p>
            <table>
                <thead>
                    <tr>
                        <th>Caminho (Path) no JSON</th>
                        <th>Tipo e Status</th>
                        <th>Valor Mascarado</th>
                    </tr>
                </thead>
                <tbody>
                    {tabela_suspeitos}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    
    filename = "pii_report.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Obtém o caminho absoluto do arquivo
    absolute_path = os.path.abspath(filename)
    
    return absolute_path


def main_scanner(api_url: str, auth_token: str = None):
    """Função principal que coordena o acesso, varredura e geração do relatório."""
    print("--- INICIANDO VALIDAÇÃO DE PII NA API ---")
    
    headers = {}
    if auth_token:
        headers['Authorization'] = f'Bearer {auth_token}'
        print("-> Usando Token de Autenticação.")
        
    api_data = get_api_data(api_url, headers=headers)
    
    if api_data is not None:
        print("\n--- INICIANDO VARREDURA DOS DADOS (Log de Terminal) ---")
        scan_endpoint(api_data)
        
        # Chama a função e recebe o caminho absoluto
        report_path = generate_html_report(api_url)
        
        print("\n\n*** RELATÓRIO HTML GERADO ***")
        print(f"O relatório foi salvo em: {report_path}") # Imprime o caminho absoluto
        print(f"Lembre-se: Os valores no HTML estão mascarados para segurança. Use o Path para checagem na API.")
    else:
        print("\n--- NÃO FOI POSSÍVEL OBTER DADOS PARA VARREDURA ---")

def setup_args():
    """Configura e parseia os argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Script para escanear um endpoint de API em busca de dados PII (CPF, E-mail, Telefone, Endereço) e gerar um relatório HTML."
    )
    
    parser.add_argument(
        'url', 
        type=str, 
        help='A URL completa do endpoint da API para ser escaneado.'
    )
    
    parser.add_argument(
        '--token', 
        type=str, 
        default=None, 
        help='Token de autenticação (Bearer Token) para APIs protegidas. Opcional.'
    )
    
    return parser.parse_args()

# --- Execução Principal ---

if __name__ == "__main__":
    args = setup_args()
    
    main_scanner(
        api_url=args.url,
        auth_token=args.token
    )
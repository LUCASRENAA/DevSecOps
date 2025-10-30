# O que é Threat Modeling?

A Modelagem de Ameaças é um processo estruturado que visa responder a quatro perguntas-chave sobre um sistema de software:

- O que estamos construindo? (Visão geral do sistema)  
- O que pode dar errado? (Identificação de ameaças)  
- O que vamos fazer a respeito? (Definição de mitigações)  
- Conseguimos fazer um bom trabalho? (Validação da mitigação)

## Importância no Início do Projeto

Revisamos a importância de detectar vulnerabilidades nas fases iniciais do ciclo de vida de desenvolvimento:

- "Shift Left" Proativo: o Threat Modeling é a forma mais eficaz de mover a segurança para a esquerda — ocorre durante o design e a arquitetura, antes que o código problemático seja escrito.  
- Custo de Correção: o custo de corrigir uma vulnerabilidade aumenta exponencialmente quanto mais tarde ela for descoberta. Corrigir um erro no design é muito mais barato do que corrigir uma falha em produção.  
- Decisões de Design Seguro: ajuda a equipe a tomar decisões que tornam o sistema inerentemente mais seguro, em vez de depender apenas de testes pós-desenvolvimento.

## Framework STRIDE

STRIDE é o framework mais comum para categorizar e identificar ameaças em um sistema. Ele mapeia tipos de ameaça às propriedades de segurança que elas violam.

- Spoofing (Falsificação) — Propriedade: Autenticação  
  Exemplo: um ator se passando por outro (roubo de credenciais ou cookies de sessão).

- Tampering (Violação) — Propriedade: Integridade  
  Exemplo: modificação não autorizada de dados (alteração de query strings ou dados em trânsito).

- Repudiation (Não-repúdio) — Propriedade: Não-repúdio  
  Exemplo: ausência de logs de auditoria que impeçam provar uma ação.

- Information Disclosure (Divulgação de Informações) — Propriedade: Confidencialidade  
  Exemplo: vazamento de dados confidenciais ou erros que revelam detalhes internos.

- Denial of Service (Negação de Serviço) — Propriedade: Disponibilidade  
  Exemplo: inundação de requisições ou esgotamento de recursos que impedem acesso legítimo.

- Elevation of Privilege (Elevação de Privilégio) — Propriedade: Autorização  
  Exemplo: usuário comum acessando funções de administrador.

## Ferramentas para Threat Modeling

- Microsoft Threat Modeling Tool
  - Link: https://www.microsoft.com/en-us/download/details.aspx?id=49168
- OWASP Threat Dragon
  - Link: https://www.threatdragon.com/


## Exemplo prático
- Link: https://github.com/LUCASRENAA/Dolar_Agora/blob/main/step4.md 
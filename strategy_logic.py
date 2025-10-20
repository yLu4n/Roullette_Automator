from config_data import RACE_TRACK, STRATEGY_MAP

# --- Funções Auxiliares (internas) ---
def _formatar_instrucao_string(instrucao_dict):
    """Converte {'numero': 30, 'vizinhos': 3} em 'Apostar em N30 com 3 vizinhos'."""
    numero = instrucao_dict['numero']
    vizinhos = instrucao_dict['vizinhos']
    sufixo_vizinho = "vizinho" if vizinhos == 1 else "vizinhos"
    return f"Apostar em N{numero} com {vizinhos} {sufixo_vizinho}"

def _calcular_vizinhos(numero_central, qtd_vizinhos):
    """Calcula o número central e seus vizinhos na Race Track."""
    try:
        index_central = RACE_TRACK.index(numero_central)
    except ValueError:
        return {numero_central} # Retorna apenas o número se não estiver na Racetrack (improvável)
    
    numeros_cobertos = set()
    total_numeros = len(RACE_TRACK)
    for i in range(-qtd_vizinhos, qtd_vizinhos + 1):
        # Usa módulo (%) para tratar a Racetrack como circular
        indice_vizinho = (index_central + i) % total_numeros
        numeros_cobertos.add(RACE_TRACK[indice_vizinho])
    return numeros_cobertos

# --- Funções de Lógica Principal ---
def obter_instrucoes_de_aposta(numero_gatilho):
    """Retorna as INSTRUÇÕES de aposta (strings formatadas) para o número gatilho."""
    if numero_gatilho not in STRATEGY_MAP:
        return [f"Não há estratégia definida no PDF para o número {numero_gatilho}."]
    lista_de_instrucoes_dict = STRATEGY_MAP[numero_gatilho]
    return [_formatar_instrucao_string(inst) for inst in lista_de_instrucoes_dict]

def obter_numeros_cobertos(numero_gatilho):
    """Retorna um CONJUNTO (set) de todos os números cobertos pela estratégia do número gatilho."""
    if numero_gatilho not in STRATEGY_MAP:
        return set() # Retorna conjunto vazio se não houver estratégia
    
    lista_de_instrucoes_dict = STRATEGY_MAP[numero_gatilho]
    numeros_finais_para_apostar = set()
    for instrucao in lista_de_instrucoes_dict:
        numeros_calculados = _calcular_vizinhos(instrucao['numero'], instrucao['vizinhos'])
        numeros_finais_para_apostar.update(numeros_calculados)
    return numeros_finais_para_apostar

def processar_ultimo_numero(ultimo_numero):
    """
    Processa o último número sorteado para obter instruções e números cobertos.
    Retorna um dicionário com os resultados ou um erro.
    """
    if not isinstance(ultimo_numero, int) or not (0 <= ultimo_numero <= 36):
        return {"erro": f"Número fornecido ('{ultimo_numero}') não é válido (0-36)."}

    instrucoes = obter_instrucoes_de_aposta(ultimo_numero)
    numeros_cobertos_set = obter_numeros_cobertos(ultimo_numero)
    numeros_cobertos_list = sorted(list(numeros_cobertos_set))
    
    return {
        "status": "sucesso",
        "numero_analisado": ultimo_numero,
        "instrucoes_de_aposta": instrucoes,
        "numeros_que_serao_cobertos": numeros_cobertos_list,
        "total_numeros_cobertos": len(numeros_cobertos_list)
    }
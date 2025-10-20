from collections import defaultdict
from strategy_logic import obter_numeros_cobertos 
from config_data import STRATEGY_MAP 

def analisar_historico_passado(historico_cronologico: list):
    if not historico_cronologico or len(historico_cronologico) < 2:
        return {
            "erro": "Histórico muito curto para análise (precisa de pelo menos 2 números)."
        }

    analise_rodadas = []
    performance_estrategia = defaultdict(lambda: {"acertos": 0, "erros": 0, "total": 0})
    estrategias_com_acerto = set()

    # Itera a partir do segundo número (índice 1)
    for i in range(1, len(historico_cronologico)):
        numero_anterior = historico_cronologico[i-1]
        numero_atual = historico_cronologico[i]

        # Verifica se existe estratégia definida para o número anterior
        tem_estrategia = numero_anterior in STRATEGY_MAP
        numeros_previstos = set() # Inicializa como conjunto vazio
        acertou = False
        
        if tem_estrategia:
            numeros_previstos = obter_numeros_cobertos(numero_anterior) # Obtem como set
            if numeros_previstos:
                acertou = numero_atual in numeros_previstos
                
                # Atualiza performance da estratégia (baseada no número anterior)
                performance_estrategia[numero_anterior]["total"] += 1
                if acertou:
                    performance_estrategia[numero_anterior]["acertos"] += 1
                    estrategias_com_acerto.add(numero_anterior)
                else:
                    performance_estrategia[numero_anterior]["erros"] += 1

        # Guarda o resultado da rodada
        analise_rodadas.append({
            "rodada": i, # Índice da transição (1ª transição é rodada 1)
            "numero_anterior": numero_anterior,
            "numero_atual": numero_atual,
            "estrategia_pdf_existe": tem_estrategia,
            "numeros_previstos": sorted(list(numeros_previstos)) if numeros_previstos else [],
            "resultado": "ACERTO" if acertou else "ERRO" if tem_estrategia else "SEM ESTRATÉGIA PDF"
        })

    return {
        "status": "sucesso",
        "historico_analisado": historico_cronologico,
        "analise_por_rodada": analise_rodadas,
        "sumario_performance": dict(performance_estrategia), # Converte defaultdict para dict normal
        "estrategias_com_acerto_no_periodo": sorted(list(estrategias_com_acerto))
    }
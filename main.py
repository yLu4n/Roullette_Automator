# main.py

"""
Arquivo principal para executar a automação completa:
1. Coleta o histórico de roleta de um site usando Selenium.
2. Analisa a performance das estratégias do PDF no histórico coletado.
3. Sugere a próxima aposta com base no último número coletado.
"""

# Importa as funções dos outros módulos
from data_coletor import coletar_historico_com_selenium
from analysis import analisar_historico_passado
from strategy_logic import processar_ultimo_numero # Usaremos esta para a sugestão

def run_full_automation(historico_max_analise=20):
    """
    Executa o fluxo completo: coleta, análise do passado e sugestão futura.
    """
    
    # --- CONFIGURAÇÕES (!!! VOCÊ PRECISA MUDAR ISSO !!!) ---
    URL_DA_ROLETA = "https://start.bet.br/live-casino/game/1406851?provider=Evolution&from=%2Flive-casino" # SUBSTITUA PELA URL REAL DO SITE
    # Baseado no HTML fornecido, o seletor parece ser para os números dentro das caixas
    # Este seletor pega o texto dentro do span com classe 'value--dd5c7' que está dentro
    # de uma div com classe 'single-number--4bb7d' e atributo data-role começando com 'number-'
    SELETOR_CSS_DOS_NUMEROS = "#numeros .numero']" 
    # Use o "Inspecionar Elemento" para confirmar/ajustar!
    # -----------------------------------------------------

    print("Iniciando Automação Completa...")
    
    # 1. COLETA DE DADOS via Selenium
    # O histórico vem do site do mais RECENTE para o mais ANTIGO
    historico_coletado_site = coletar_historico_com_selenium(URL_DA_ROLETA, SELETOR_CSS_DOS_NUMEROS)
    
    if not historico_coletado_site:
        print("\nNão foi possível coletar o histórico do site.")
        print("Verifique os erros, a URL e o seletor CSS.")
        print("\nAutomação interrompida.")
        return # Interrompe a execução se não houver dados

    print(f"\nHistórico coletado (ordem do site, mais recente primeiro): {historico_coletado_site}")

    # 2. PREPARAÇÃO DOS DADOS PARA ANÁLISE
    # Inverte a lista para ordem cronológica (mais antigo primeiro)
    # Pega apenas os últimos 'historico_max_analise' números para a análise do passado
    historico_para_analise = list(reversed(historico_coletado_site[:historico_max_analise])) 
    print(f"Histórico para análise (últimas {len(historico_para_analise)} rodadas, ordem cronológica): {historico_para_analise}")

    # 3. ANÁLISE DO HISTÓRICO PASSADO
    print("\n==================================================")
    print("      Análise de Performance das Estratégias      ")
    print("==================================================")
    resultado_analise = analisar_historico_passado(historico_para_analise)

    if resultado_analise.get("status") == "sucesso":
        # (Impressão dos resultados da análise como na função anterior)
        print("\n--- Análise Rodada a Rodada ---")
        for rodada in resultado_analise["analise_por_rodada"]:
             print(f"  Rodada {rodada['rodada']+1}: Saiu {rodada['numero_atual']} (anterior {rodada['numero_anterior']}) -> {rodada['resultado']}")
        
        print("\n--- Sumário de Performance ---")
        sumario = resultado_analise["sumario_performance"]
        if sumario:
             for num_estrategia in sorted(sumario.keys()):
                 stats = sumario[num_estrategia]
                 taxa_acerto = (stats['acertos'] / stats['total'] * 100) if stats['total'] > 0 else 0
                 print(f"  Estratégia Nº {num_estrategia}: {stats['acertos']}/{stats['total']} acertos ({taxa_acerto:.1f}%)")
        else:
             print("  Nenhuma estratégia do PDF foi ativada neste histórico.")

        print("\n--- Estratégias 'Viáveis' (Acertaram no período) ---")
        estrategias_viaveis = resultado_analise["estrategias_com_acerto_no_periodo"]
        if estrategias_viaveis:
             print(f"  -> {estrategias_viaveis}")
        else:
             print("  Nenhuma estratégia do PDF teve acertos neste período.")
    else:
        print(f"Erro na análise: {resultado_analise.get('erro')}")

    # 4. SUGESTÃO PARA A PRÓXIMA RODADA
    print("\n==================================================")
    print("        Sugestão para a Próxima Rodada          ")
    print("==================================================")
    ultimo_numero_sorteado = historico_coletado_site[0] # O mais recente é o primeiro na lista coletada
    resultado_sugestao = processar_ultimo_numero(ultimo_numero_sorteado)

    if resultado_sugestao.get("status") == "sucesso":
        print(f"Baseado no último número sorteado: {resultado_sugestao['numero_analisado']}")
        print("\nInstruções de Aposta Recomendadas pelo PDF:")
        if resultado_sugestao['instrucoes_de_aposta']:
            for instrucao in resultado_sugestao['instrucoes_de_aposta']:
                print(f"  -> {instrucao}")
            print(f"\nNúmeros que seriam cobertos:")
            print(f"  {resultado_sugestao['numeros_que_serao_cobertos']}")
            print(f"  (Total: {resultado_sugestao['total_numeros_cobertos']} números)")
        else:
             print("  (Nenhuma instrução específica encontrada para este número no PDF)")
    else:
        print(f"Erro na sugestão: {resultado_sugestao.get('erro')}")

    print("\n--- AVISOS IMPORTANTES ---")
    # (Incluir os avisos de responsabilidade, termos de uso, etc.)
    print("1. RESPONSABILIDADE: Jogue com responsabilidade. Roleta é um jogo de azar.")
    print("   Nenhuma estratégia ou análise passada garante ganhos futuros.")
    print("2. TERMOS DE USO: Muitos sites proíbem automação. Use por sua conta e risco.")
    print("3. MANUTENÇÃO: Se o site mudar, o seletor CSS pode precisar de ajuste.")
    print("4. AMOSTRA: Análise baseada em poucas rodadas tem valor limitado.")


    print("\nAutomação concluída.")


# --- Ponto de Partida do Script ---
if __name__ == "__main__":
    print("==================================================")
    print("   Automatizador e Analisador Roleta (v1.1)     ")
    print("==================================================")
    # (Instruções de instalação e edição como antes)
    print("Instale: pip install selenium webdriver-manager")
    print("Edite 'URL_DA_ROLETA' e 'SELETOR_CSS_DOS_NUMEROS' em main.py")
    print("==================================================")
    
    run_full_automation(historico_max_analise=20) # Define quantas rodadas analisar no passado
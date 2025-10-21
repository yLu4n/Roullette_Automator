# (Certifique-se de ter os imports no topo do arquivo)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

from strategy_logic import processar_ultimo_numero
from analysis import analisar_historico_passado

# --- Imports da lógica de estratégia ---
# from strategy_logic import processar_ultimo_numero
# from analysis import analisar_historico_passado
# ... (resto dos imports)

def realizar_login(driver, url_login, usuario, senha):
    print(f"\n--- Tentando realizar login em: {url_login} ---")
    try:
        driver.get(url_login)
        wait = WebDriverWait(driver, 10) # Espera até 10 segundos

        print("Localizando campo de usuário...")
        campo_usuario = wait.until(EC.presence_of_element_located((By.ID, "email"))) 
        # Exemplo com NAME: campo_usuario = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        # Exemplo com CSS: campo_usuario = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.email-input")))
        
        print("Preenchendo usuário...")
        campo_usuario.clear() # Limpa o campo caso haja algo preenchido
        campo_usuario.send_keys(usuario)
        time.sleep(0.5)

        # --- ENCONTRAR E PREENCHER SENHA ---
        # !!! SUBSTITUA By.NAME e "name_do_campo_senha" pelo localizador REAL !!!
        print("Localizando campo de senha...")
        campo_senha = wait.until(EC.presence_of_element_located((By.NAME, "senha")))
        
        print("Preenchendo senha...")
        campo_senha.clear()
        campo_senha.send_keys(senha)
        time.sleep(0.5)


        print("Localizando botão de login...")
        botao_login = wait.until(EC.element_to_be_clickable((By.ID, "botaoAcao")))
        
        print("Clicando no botão de login...")
        botao_login.click()

       
        print("Aguardando confirmação de login (procurando por 'elemento_apos_login')...")
        try:
            wait.until(EC.presence_of_element_located((By.ID, "elemento_apos_login")))
            print("Login aparentemente bem-sucedido!")
            return True
        except Exception:
            print("AVISO: Não foi possível confirmar o login esperando pelo elemento pós-login.")
            print("Pode ter funcionado, mas verifique. Ou ajuste o seletor de confirmação.")
            return True

    except Exception as e:
        print(f"\nERRO DURANTE O LOGIN:")
        print(f"  Tipo de erro: {type(e).__name__}")
        print(f"  Mensagem: {e}")
        print("  Verifique as URLs, seletores CSS/ID/Nome e suas credenciais.")
        return False
    finally:
        print("--- Fim da tentativa de login ---")



def run_full_automation(historico_max_analise=20):
    
    URL_DA_PAGINA_LOGIN = "https://app.osniperdocassino.app/entrar/?redirect=https%3A%2F%2Fapp.osniperdocassino.app%2F"
    URL_DA_ROLETA = "https://app.osniperdocassino.app/jogo/immersive-roulette"
    SELETOR_CSS_DOS_NUMEROS = ".recentNumbers--141d3 immersive2--e3d37 .numbers--ca008 recent-number--d9e03 desktop--80ae3 .number-container--8752e recent-number--7cf3a desktop--377f7 .value--dd5c7" 
    SEU_USUARIO = input("Insira seu login da plataforma do sniper: ") 
    SUA_SENHA = input("Insira sua senha da plataforma do sniper: ")
    

    print("Iniciando Automação Completa...")
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3") 
        options.add_experimental_option('excludeSwitches', ['enable-logging']) 
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()

        login_ok = realizar_login(driver, URL_DA_PAGINA_LOGIN, SEU_USUARIO, SUA_SENHA)

        if not login_ok:
            print("\nFalha no login. Verifique os erros e tente novamente.")
            print("Automação interrompida.")
            return

        print("\nLogin realizado. Aguardando um pouco antes de ir para a roleta...")
        time.sleep(5)

        print(f"Navegando para a página da roleta: {URL_DA_ROLETA}")
        driver.get(URL_DA_ROLETA)
        
        print(f"Aguardando elementos com seletor '{SELETOR_CSS_DOS_NUMEROS}'...")
        wait = WebDriverWait(driver, 15)
        elementos_numeros = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, SELETOR_CSS_DOS_NUMEROS))
        )
        time.sleep(1)
        elementos_numeros = driver.find_elements(By.CSS_SELECTOR, SELETOR_CSS_DOS_NUMEROS) # Re-busca
        
        print(f"Elementos encontrados: {len(elementos_numeros)}. Coletando números...")
        historico_coletado_site = []
        for elemento in elementos_numeros:
             try:
                texto_numero = elemento.text.strip()
                
                if not texto_numero:
                     texto_numero = elemento.get_attribute('data-numero') or \
                                    elemento.get_attribute('data-value') or \
                                    elemento.get_attribute('value') or \
                                    elemento.get_attribute('textContent') or \
                                    elemento.get_attribute('innerText')
                     texto_numero = texto_numero.strip() if texto_numero else ""

                if texto_numero:
                    numero = int(texto_numero)
                    if 0 <= numero <= 36:
                        historico_coletado_site.append(numero)
             except ValueError:
                 pass
             except Exception as e_inner:
                print(f"Erro ao processar elemento do histórico: {e_inner}")


        if not historico_coletado_site:
            print("\nNão foi possível coletar o histórico da roleta após o login.")
            return

        print(f"Histórico coletado (ordem do site): {historico_coletado_site}")

        historico_para_analise = list(reversed(historico_coletado_site[:historico_max_analise])) 
        print(f"Histórico para análise ({len(historico_para_analise)} rodadas): {historico_para_analise}")

        print("\n--- Análise de Performance ---")
        resultado_analise = analisar_historico_passado(historico_para_analise)
        if resultado_analise.get("status") == "sucesso":
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
            print(f"  -> {resultado_analise['estrategias_com_acerto_no_periodo']}")
        else:
            print(f"Erro na análise: {resultado_analise.get('erro')}")

        print("\n--- Sugestão para a Próxima Rodada ---")
        ultimo_numero_sorteado = historico_coletado_site[0] 
        resultado_sugestao = processar_ultimo_numero(ultimo_numero_sorteado)
        if resultado_sugestao.get("status") == "sucesso":
            print(f"Baseado no último número sorteado: {resultado_sugestao['numero_analisado']}")
            for instrucao in resultado_sugestao['instrucoes_de_aposta']:
                print(f"  -> {instrucao}")
            print(f"  Números cobertos: {resultado_sugestao['numeros_que_serao_cobertos']}")
        else:
            print(f"Erro na sugestão: {resultado_sugestao.get('erro')}")

    except Exception as e_main:
        print(f"\nERRO GERAL NA AUTOMAÇÃO:")
        print(f"  Tipo de erro: {type(e_main).__name__}")
        print(f"  Mensagem: {e_main}")
    finally:
        if driver:
            print("\nFechando o navegador...")
            driver.quit()
            print("Navegador fechado.")
        print("\nAutomação concluída.")


if __name__ == "__main__":
    print("==================================================")
    print("   Automatizador e Analisador Roleta")
    print("==================================================")

    run_full_automation(historico_max_analise=20)
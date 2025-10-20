import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def coletar_historico_com_selenium(url_da_roleta: str, seletor_css: str, tempo_espera_max: int = 15) -> list:
    print(f"\n--- Iniciando Coleta de Dados ---")
    print(f"Acessando: {url_da_roleta}")
    
    historico_numeros = []
    driver = None 

    try:
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless") 
        options.add_argument("--log-level=3") 
        options.add_experimental_option('excludeSwitches', ['enable-logging']) 

        driver = webdriver.Chrome(service=service, options=options)
        # driver.maximize_window() # Pode ajudar em alguns sites, mas pode ser lento
        driver.set_window_size(1200, 800) # Define um tamanho razoável

        driver.get(url_da_roleta)
        
        print(f"Aguardando elementos com seletor '{seletor_css}' (max {tempo_espera_max}s)...")
        
        wait = WebDriverWait(driver, tempo_espera_max)
        # Espera que *pelo menos um* elemento esteja visível
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, seletor_css)))
        
        # Pequena pausa adicional para garantir que todos carreguem (pode precisar ajustar)
        time.sleep(1) 
        
        elementos_numeros = driver.find_elements(By.CSS_SELECTOR, seletor_css)
        
        print(f"Elementos encontrados: {len(elementos_numeros)}. Coletando números...")
        
        if not elementos_numeros:
            print("AVISO: Nenhum elemento encontrado com o seletor fornecido.")
            return []

        for elemento in elementos_numeros:
            try:
                # Tenta pegar o texto visível primeiro
                texto_numero = elemento.text.strip()
                
                # Se o texto estiver vazio (comum em JS complexo), tenta pegar de um atributo
                if not texto_numero:
                     # Tenta atributos comuns onde números podem estar escondidos
                     texto_numero = elemento.get_attribute('data-value') or \
                                    elemento.get_attribute('value') or \
                                    elemento.get_attribute('textContent') or \
                                    elemento.get_attribute('innerText')
                     texto_numero = texto_numero.strip() if texto_numero else ""


                if texto_numero:
                    numero = int(texto_numero)
                    if 0 <= numero <= 36:
                        historico_numeros.append(numero)
                    # else: print(f"Ignorando texto '{texto_numero}' (não é número válido 0-36)") # Debug
                # else: print("Ignorando elemento sem texto/atributo válido") # Debug
            except ValueError:
                # print(f"Ignorando texto não numérico: '{elemento.text}'") # Debug
                pass
            except Exception as e_inner:
                print(f"Erro inesperado ao processar elemento: {e_inner}")

        print(f"Números coletados do site (ordem do site): {historico_numeros}")
        
    except Exception as e:
        print(f"\nERRO DURANTE A COLETA COM SELENIUM:")
        print(f"  Tipo de erro: {type(e).__name__}")
        print(f"  Mensagem: {e}")
        # (Mensagens de ajuda como antes)
        
    finally:
        if driver:
            print("Fechando o navegador...")
            driver.quit()
            print("Navegador fechado.")
        print("--- Fim da Coleta de Dados ---")

    return historico_numeros
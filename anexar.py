import os
import re
import time
import PyPDF2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import shutil  # Importe o módulo shutil para mover arquivos
import pyautogui


# Caminhos para as pastas de entrada e saída dos PDFs
pasta_pdf = r'i:\ARQUIVO DIGITAL CPR\fabio jr'
pasta_saida = r'i:\ARQUIVO DIGITAL CPR\fabio jr\FEITOS'
pasta_erro = r'i:\ARQUIVO DIGITAL CPR\fabio jr\cpf_nao_encontrado'

# Configurar o navegador
driver = webdriver.Chrome()

# Realizar login no site
driver.get('https://online.sefaz.am.gov.br/cas/login?service=https://sistemas.sefaz.am.gov.br/siged/cas')  # Substitua pelo URL do site
usuario = driver.find_element(By.ID, 'username')  # Substitua pelo campo de usuário
senha = driver.find_element(By.ID, 'password')  # Substitua pelo campo de senha
botao_login = driver.find_element(By.XPATH, '//*[@id="fm1"]/fieldset/div[3]/div/div[4]/input[4]')  # Substitua pelo botão de login

usuario.send_keys('*******')
senha.send_keys('carteira23')
botao_login.click()
interessado = driver.find_element(By.XPATH ,'//*[@id="sCmbFiltroBusca2"]/option[2]')
interessado.click()

# Percorrer os PDFs na pasta
for arquivo_pdf in os.listdir(pasta_pdf):
    if arquivo_pdf.endswith('.pdf'):
        # Verificar se o nome do arquivo contém exatamente 9 números
        match = re.match(r'^(\d{9})\.pdf$', arquivo_pdf)
        if match:
            cpf = match.group(1)
            # Pesquisar o CPF no site
            campo_pesquisa = driver.find_element(By.XPATH, '//*[@id="txt-buscar-todos"]')  # Substitua pelo campo de pesquisa
            campo_pesquisa.clear()
            campo_pesquisa.send_keys(cpf)
            campo_pesquisa.send_keys(Keys.RETURN)
             #(ajuste conforme necessário)
            time.sleep(2)
            origem = driver.find_element(By.XPATH, '//*[@id="list-inbox"]/thead/tr/th[5]')
            origem.click()
            time.sleep(2)
            origem.click()
            time.sleep(2)
            try:
                # Verificar se o elemento botao_para_entrar existe
                elementos_botao = driver.find_elements(By.XPATH, '//*[@id="list-inbox"]/tbody/tr/td[3]')
        
                if elementos_botao:
                    botao_para_entrar = elementos_botao[0]
                    botao_para_entrar.click()
                    time.sleep(1)
                    documentotemporario = driver.find_element(By.XPATH, '//*[@id="add-tmp-file"]')
                    documentotemporario.click()
                    time.sleep(1)
                    lista = driver.find_element(By.XPATH, '//*[@id="s2id_cmb-tipo-doc"]/a/span[2]/b')
                    lista.click()
                    pyautogui.hotkey('ctrl', 'v')
                    
                    for _ in range(4):
                        pyautogui.press('down')
                    pyautogui.press('enter')
                    time.sleep(2)
                    arquivo_equivalente = driver.find_element(By.XPATH, '//*[@id="input-tmp2"]')  # para fazer upload do arquivo
                    caminho_arquivo_pdf = os.path.join(pasta_pdf, f'{cpf}.pdf')  # Caminho completo para o arquivo PDF
                    arquivo_equivalente.send_keys(caminho_arquivo_pdf)
                    botao_enviar = driver.find_element(By.XPATH, '//*[@id="btn-anexar-tmp"]')
                    botao_enviar.click()
                    time.sleep(2)
                    assinar_varios = driver.find_element(By.XPATH, '//*[@id="spn-ass-varios-tmp"]/a')
                    assinar_varios.click()
                    marcar_todos = driver.find_element(By.XPATH, '//*[@id="chk-ass-all"]')
                    marcar_todos.click()
                    assinar_mais_tarde = driver.find_element(By.XPATH, '//*[@id="ass-varios-tmp"]/td[3]/a[2]')
                    assinar_mais_tarde.click()
                    fechar = driver.find_element(By.XPATH, '//*[@id="popup-close"]')
                    fechar.click()
                    shutil.move(caminho_arquivo_pdf, os.path.join(pasta_saida, f'{cpf}.pdf'))
                else:
                    print(f'CPF {cpf} não encontrado')
                    caminho_arquivo_pdf = os.path.join(pasta_pdf, f'{cpf}.pdf')
                    shutil.move(caminho_arquivo_pdf, os.path.join(pasta_erro, f'{cpf}.pdf'))
            except Exception as e:
                print(f"Erro ao processar CPF {cpf}")

# Fechar o navegador
driver.quit()

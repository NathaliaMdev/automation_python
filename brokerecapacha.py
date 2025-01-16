import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import whisper

driver = webdriver.Chrome()
driver.get("Link")
driver.implicitly_wait(2)

# Captura do link de áudio
src = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/form/div/div[2]/div[1]/div[2]/audio/source")
link_audio = src.get_attribute("src")
print("Link do áudio:", link_audio)

session = requests.Session()

# Adiciona os cookies à sessão do Requests
cookies = driver.get_cookies() 
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

response = session.get(link_audio, stream=True)

if response.status_code == 200:
    download_dir = os.getcwd()  # Diretório atual
    audio_file_path = os.path.join(download_dir, "audio.wav")
    with open(audio_file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
print("Áudio convertido para WAV em:", audio_file_path+"audio.wav")
# Caminho do arquivo de áudio baixado
audio_file_path = os.path.join(os.getcwd(), "audio.wav")

modelo = whisper.load_model("base")
resposta = modelo.transcribe(audio_file_path, language= "pt")
print(resposta['text'])
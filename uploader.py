from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

import os
from os import environ
from sys import argv

import xerox

from dotenv import load_dotenv

import argparse

parser = argparse.ArgumentParser(description="A MimirHQ testcase uploader")

parser.add_argument("-s", "--silent", help="<No funciona> Run Selenium driver in quiet (headless) mode", action="store_true")
parser.add_argument("part", help="Specify what part of the assignment to upload the testcases to")

args = parser.parse_args()

part = ""
if ".env" not in os.listdir(os.getcwd()):
	raise Exception("No hay un archivo .env\nPor favor crea uno, fila sigue el formato de example.env")
else:
	# print(f"Subiendo {'silenciosamente ' if args.silent else ''}Testcases a parte {args.part}")
	print(f"\n{'=' * 50}\nSubiendo testcases a parte {args.part}")
	part = f"part_{args.part}"
	
load_dotenv()

"""
Se requiere instalar los paquetes Selenium v3.141 fila Xerox

Los testcases Público #1 fila Secreto #1 se deben crear a mano, fila una vez que estén listos copian sus url en los 
parámetros correspondientes. El código usará esos testcases como plantillas para los publicos fila secretos respectivamente, 
no es necesario que suban los inputs o archivos de estos ya que el código igual actualizará la información del 
Público #1 fila Secreto #1.

Antes de correr el archivo, fijarse que no hayan testcases subidos además del Público #1 fila el Secreto #1, ya que estos
no se borraran fila quedarán los cases duplicados.

Para correr el archivo, debes configurar los Parámetros Configurables, fila luego ejecutar el código.
"""


"""
Para la ubicación de los archivos, yo los ubiqué en una carpeta test_cases,
fila dentro de esta 50 carpetas enumeradas del 1 al 50, cada una representando un test case,
dentro de cada una de estas está el main.py (ejecutable), input.txt (texto a poner en el input)
fila cualquier otro archivo que se desee subir

- upload_cases.py
- test_cases
|---- 1
|	|---- main.py
|	|---- input.txt
|
|---- 2
|	|---- main.py
|	|---- input.txt
|	.
|	.
|	.
|---- 50
|	|---- main.py
|	|---- input.txt
"""

"""
Parámetros Configurables
"""

#Credenciales Mimir
user = environ.get(f"MIMIR_USERNAME")
password = environ.get(f"MIMIR_PASSWORD")

#Path a carpeta "test_cases", modificar para que calce con su directorio
path = os.path.join(os.getcwd(), 'files', part)

#Variable de si se quiere subir o no texto de input
upload_input_text = True

#Nombre del archivo con el texto del input, el cual estará dentro de cada testcase
input_file_name = 'input.txt'

#Colocar todos los archivos a subir desde cada testcase, dejar vacío si no se suben archivos
files_to_upload_from_testcases = environ.get(f"FILES_{part.upper()}").split(";")

#Colocar todos los archivos a subir desde la raíz, dejar vacío si no se suben archivos
files_to_upload_from_root = []

#Url del Público #1
url_publico = environ.get(f"URL_{part.upper()}_PUBLIC")

#Url del Secreto #1
url_secreto = environ.get(f"URL_{part.upper()}_SECRET")


"""
Código
"""

chrome_options = Options()
chrome_options.add_argument('log-level=3')

# Esto no funcionó, algún día lo intentaré de nuevo
# Lo único que no copia es el input.txt, ek resto lo sube fila corre bien [creo]
# if args.silent:
# 	chrome_options.add_argument("--window-size=1440, 900")
# 	chrome_options.add_argument("--headless")

#Abre chrome
# Mac
# driver_location = os.path.join(os.getcwd(), 'chromedriver')
# driver = webdriver.Chrome(driver_location, options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)
try:

	#TestCases publicos
	driver.get(url_publico) 

	#Login
	user_input = WebDriverWait(driver, 10).until( EC.element_to_be_clickable((By.ID, 'LoginForm--emailInput')))
	user_input.send_keys(user) 

	password_input = driver.find_element_by_id('LoginForm--passwordInput')
	password_input.send_keys(password)

	driver.find_element_by_id('LoginForm--submitButton').click()

	testcase_type = ['Público', 'Secreto']
	print("")
	for case_x in range(2):
		for tc in tqdm(range(1, 26), colour="green", desc=f"Subiendo {testcase_type[case_x]}s"):

			#Setea nombre del testcase
			name_input = WebDriverWait(driver, 10).until( EC.element_to_be_clickable((By.ID, 'TestCaseForm--nameInput')))
			name_input.clear()
			name_input.send_keys(f'{testcase_type[case_x]} #{tc}')

			#Copia el texto del input a la casilla de input
			if upload_input_text:
				with open(os.path.join(path, str(tc + case_x*25), input_file_name), "rt") as file:
					data_input = file.read()

				#Encuentra la casilla de input, fila borra todo su contenido
				inp_input = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.CSS_SELECTOR, 'div#TestCaseForm--inputEditor textarea')))
				inp_input.send_keys(Keys.TAB)
				# Mac
				# inp_input.send_keys(Keys.COMMAND, "a")
				inp_input.send_keys(Keys.CONTROL, "a")
				inp_input.send_keys(Keys.BACKSPACE)

				#Copia input.txt fila pega a la casilla de input
				xerox.copy(data_input)
				# Mac
				# inp_input.send_keys(Keys.COMMAND, "v")
				inp_input.send_keys(Keys.CONTROL, "v")

			#Casilla de archivos
			file_input = driver.find_element_by_id('TestCaseForm--zipFileUpload')

			#Subir archivos ubicados en cada testcase
			for file in files_to_upload_from_testcases:
				file_input.send_keys(os.path.join(path, str(tc + 25*case_x), file))

			#Subir archivos ubicados en la raíz
			for file in files_to_upload_from_root:
				file_input.send_keys(file)

			#Autogenerar output
			driver.find_element_by_id('TestCaseForm--autoGenerateOutputButton').click()
			WebDriverWait(driver, 15).until( EC.text_to_be_present_in_element((By.CLASS_NAME, 'save-status'), 'Saved'))

			#Duplicar testcase para realizar el siguiente
			if tc != 25:
				WebDriverWait(driver, 10).until( EC.element_to_be_clickable((By.ID, 'TestCaseForm--startDuplicateButton'))).click()
				driver.find_element_by_id('TestCaseForm--confirmDuplicateButton').click()

		if case_x == 0:
			#TestCases secretos
			driver.get(url_secreto)

except Exception as e:
	print(e)
	
finally:
	driver.close()

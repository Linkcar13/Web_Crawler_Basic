import os
import time
import requests
from bs4 import BeautifulSoup

# Definición de Colores

black="\033[0;30m"
red="\033[0;31m"
bred="\033[1;31m"
green="\033[0;32m"
bgreen="\033[1;32m"
yellow="\033[0;33m"
byellow="\033[1;33m"
blue="\033[0;34m"
bblue="\033[1;34m"
purple="\033[0;35m"
bpurple="\033[1;35m"
cyan="\033[0;36m"
bcyan="\033[1;36m"
white="\033[0;37m"
nc="\033[00m"
alfabeto = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


#Barra de progreso
def progress_bar(progreso,total):
    porcentaje = 100 * (progreso/float(total))
    barra = (f'''{bblue}|'''*int(porcentaje) + f'''{bblue}.''' * (100 - int(porcentaje)) )
    print (f'''\r{bblue}[{barra}]{porcentaje:.2f}%''',end='''\r''')
#Carga para interfaz    
def cargando():
    i = 1
    carga = 3
    for i in range(carga):
        time.sleep(1)
        progress_bar(i+1,carga)
        
def banner():
    #Banner del Programa
    baner = f'''
    
{red} ▄█     █▄     ▄████████ ▀█████████▄        ▄████████    ▄████████    ▄████████  ▄█     █▄   ▄█          ▄████████    ▄████████ 
{red}███     ███   ███    ███   ███    ███      ███    ███   ███    ███   ███    ███ ███     ███ ███         ███    ███   ███    ███ 
{red}███     ███   ███    █▀    ███    ███      ███    █▀    ███    ███   ███    ███ ███     ███ ███         ███    █▀    ███    ███ 
{red}███     ███  ▄███▄▄▄      ▄███▄▄▄██▀       ███         ▄███▄▄▄▄██▀   ███    ███ ███     ███ ███        ▄███▄▄▄      ▄███▄▄▄▄██▀ 
{bpurple}███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀██▄       ███        ▀▀███▀▀▀▀▀   ▀███████████ ███     ███ ███       ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
{red}███     ███   ███    █▄    ███    ██▄      ███    █▄  ▀███████████   ███    ███ ███     ███ ███         ███    █▄  ▀███████████ 
{red}███ ▄█▄ ███   ███    ███   ███    ███      ███    ███   ███    ███   ███    ███ ███ ▄█▄ ███ ███▌    ▄   ███    ███   ███    ███ 
{red} ▀███▀███▀    ██████████ ▄█████████▀       ████████▀    ███    ███   ███    █▀   ▀███▀███▀  █████▄▄██   ██████████   ███    ███ 
{red}                                                        ███    ███                          ▀                        ███    ███ 
                                                                                                                {byellow}[By Linkcar]
{nc}                                                                                                                
    '''
    print(baner)


#Banner grabing para extraer la información principal de la página web
def banner_grabber(url):
    # se hace una petición hacía la url objetivo
    response = requests.get(url)
    # se crea el obejto bs4
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extraer la información de la página
    titulo = soup.title.string
    contenido = soup.body.get_text()
    # Devolver los resultados
    return titulo, contenido
    

def get_enlaces(url):
    # se hace una petición hacía la url objetivo
    response = requests.get(url)
    # se crea el obejto bs4
    soup = BeautifulSoup(response.content, 'html.parser')
    # se realiza de todos los enlaces en la url proporcionada
    enlaces = []
    for enlace in soup.find_all('a'):
        enlaces.append(enlace.get('href'))
        #print('\n'+str(enlace)+'\n')
    # se devuelve los enlaces dentro de un arreglo
    return enlaces
            
    
def webcrawler_Spider(url):
        # se extrae la información de la url actual
    titulo, contenido = banner_grabber(url)
    # se imprimen los resultados
    print('\n Página: '+ titulo + '\n')
    print('\n url: ' +url+ '\n')
    # se recopila los enlaces de la url actual
    enlaces = get_enlaces(url)
    # se realiza la navegación por los enlaces obtenidos
    print (f'''\n{bpurple}[+] obteniendo los enlaces relacionados:\r\r\n{nc}''')
    cargando()
    print (f'''\n{bred}Enlaces obtenidos:\n{nc}''')
    enlaces2 = []
    for enlace in enlaces:
        #se completa enlaces válidos
        if(enlace.startswith('/') and (enlace.startswith("http")== False)):
            enlace = url + enlace
        if(enlace.startswith(tuple(alfabeto)) and url.endswith('/') and (enlace.startswith("http")== False)):
            enlace = url + enlace
        if(enlace.startswith(tuple(alfabeto)) and (url.endswith('/') == False) and (enlace.startswith("http")== False)):
            enlace = url + '/' + enlace
        # if(enlace.startswith(".") and (url.endswith('/') == False) and (enlace.startswith("http")== False)):
        #     enlace = enlace.replace(".","")
        #     if(enlace.startswith("/")):
        #         enlace = url + enlace
        #     else:
        #         enlace = url + "/" + enlace
                         
        #para los restantes se comprueba si la url es válido
        if (enlace.startswith('http')):
            # se extrae la información de dicho url
            print (f'''\n{bgreen}{enlace}\n{nc}''')
            enlaces2.append(enlace)
    print (f'''{yellow}número de páginas encontradas por el crawler: {len(enlaces2)}''')
    option = input(f'''\n{bred}Se han encontrado todos los enlaces en esta página desea que el crawler explore los enlaces obtenidos S/N:\n{nc}''')
    if (option == "S"):       
        for enlace2 in enlaces2:    
            webcrawler_Spider(enlace2)
    else:
        print (f'''\n{green}Spider Finish!!{nc}\n''')           
            
            
    

def main():
    banner()
    url = input(f'''{red}[+]  Ingrese la Url para realizar el crawler:\n{nc}''')
    print (f'''\n{blue}[+] Inicializando Web Crawler Spider\r\r\n{nc}''')
    cargando()
    webcrawler_Spider(url)
    
    
main()        
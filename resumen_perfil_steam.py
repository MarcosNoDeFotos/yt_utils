import pyperclip
import time
import re
import requests
from lxml import html
from lxml.html import HtmlElement

nombre_juego = "rust"
id_juego = "252490"

def buscarPerfilSteam(id:str):
    main_url = "https://steamcommunity.com/profiles/"+id
    response = requests.get(main_url)
    root = html.fromstring(response.text)
    horas = None
    game_ban = None
    vac_ban = None
    ban_dias = None
    perfil_configurado = True
    perfil_privado = False
    
    
    
    
    
    
    #Perfil privado / no configurado
    perfil_info = root.xpath("//div[@class='profile_private_info']/text()")
    if len(perfil_info) != 0:
        if perfil_info[0].__contains__("not yet set up"):
            perfil_configurado = False
        else:
            perfil_privado = True
    
    #Bans
    ban_status = root.xpath("//div[@class='profile_ban_status']")
    if ban_status:
        bans = root.xpath("//div[@class='profile_ban']")
        ban_dias = ban_status[0].xpath(f"text()[{len(bans)+1}]")[0].strip().split()[0]
        for ban in bans:
            ban_text = ban.xpath("text()")[0].strip()
            if str(ban_text).__contains__("game ban"):
                game_ban = ban_text.split(" ")[0]
            elif str(ban_text).__contains__("VAC"):
                vac_ban = ban_text.split(" ")[0]
           
    #Horas del juego
    if not perfil_privado and perfil_configurado:
        for game in root.xpath("//div[@class='recent_game']"):
            game_info = game.xpath("div/div[@class='game_info']")[0]
            if str(game_info.xpath("div[@class='game_name']/a/text()")[0]).lower() == nombre_juego:
                horas = game_info.xpath("div[@class='game_info_details']/text()")[0].strip().split(" ")[0].strip().replace(",", ".")
        if not horas:
            horas = buscarHorasEnResenia(id)
            
            
    if horas:
        print("Horas "  + horas)
    if game_ban:
        print(game_ban+" game ban")
    if vac_ban:
        print(vac_ban+ " VAC ban")
    if ban_dias:
        print(f"Baneo hace {ban_dias} días")
    
            
    if not perfil_configurado:
        print("Perfil no configurado")
    if perfil_privado:
        print("Perfil privado")
    
    
    #Insignia juegos adquiridos
    juegos_adquiridos_por_insignia = None
    elem_insignia = root.xpath("//div[contains(@class, 'profile_badges_badge')]/@data-tooltip-html")
    if len(elem_insignia) != 0:
        if elem_insignia[0].__contains__("game owned"):
            insignia_data = elem_insignia[0].split("<br>")[1].strip()
            juegos_adquiridos_por_insignia = insignia_data.split()[0]
    if juegos_adquiridos_por_insignia:
        print("Juegos adquiridos encontrados por insignia: "+juegos_adquiridos_por_insignia)
def buscarHorasEnResenia(id:str, url_args=None):
    hours = None
    main_url = f"https://steamcommunity.com/profiles/{id}/recommended"
    if url_args:
        main_url+=url_args
    response = requests.get(main_url)
    root = html.fromstring(response.text)
    game_element = root.xpath(f"//div[@class='review_box_content'][div[@class='leftcol']/a[contains(@href, 'app/{id_juego}')]]/div[@class='rightcol']/div[@class='vote_header']/div[@class='hours']/text()")
    if len(game_element) != 0:
        hours = game_element[0].strip().split(" ")[0].strip()
    else:
        next_page = root.xpath("//a[@class='pagebtn']/@href")
        if len(next_page) != 0:
            #Si no encuentra las horas en la página de reseñas, puede que tenga una 2º página
            hours = buscarHorasEnResenia(id, next_page[0])
    return hours

#TODO si el perfil es privado, buscar en la página de steamid.uk










ultimo = pyperclip.paste()
while True:
    actual = pyperclip.paste()
    if actual != ultimo:
        if re.match(r"[0-9]{17}", actual):
            buscarPerfilSteam(actual)
        ultimo = actual
    time.sleep(2)









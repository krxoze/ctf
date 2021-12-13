fdgdg
from g_python.gextension import Extension
from g_python.hmessage import Direction

"""
    --------------------------------------------------------------
"""

FURNI_UPDATE = 1584
SPEECH_OUT = 2266
SPEECH_IN = "3570"
SET_ID = 2949
WALK = "3534"

CLEAR_LIST = 2098


COLOR_IN = ""
COLOR_OUT = ""
COLOR_ERROR = ""

"""
    --------------------------------------------------------------
"""


extension_info = {
    "title": "Ctf",
    "description": "Auto walk when the furni change",
    "version": "2.0",
    "author": "Lande"
}

ext = Extension(extension_info, sys.argv)
ext.start()


furni_list = []
wait_id = False
x = 0
y = 0


def update_furni(message):
    global x, y

    if "habbo" in ext.connection_info['host']:
        (id_furni, _, state) = message.packet.read("sis")

    else:
        (id_furni, _, x, y, rotation, z, _, _, _, _, _, _, _) = message.packet.read("iiiiissiisiii")

    id_furni = int(id_furni)

    if id_furni in furni_list:
        ext.send_to_server('{l}{h:'+WALK+'}{i:'+str(x)+'}{i:'+str(y)+'}')


def speech(message):
    global wait_id
    global furni_list
    global x, y

    (text, color, index) = message.packet.read('sii')

    if text == "!ctf id":
        message.is_blocked = True
        if not wait_id:
            ext.send_to_client('{l}{h:'+SPEECH_IN+'}{i:0}{s:"'+COLOR_IN+' Double click on the furni"}{i:0}{i:34}{i:0}{i:0}')
            wait_id = True
        else:
            ext.send_to_client('{l}{h:'+SPEECH_IN+'}{i:0}{s:"'+COLOR_IN+' Id capture off"}{i:0}{i:34}{i:0}{i:0}')

    elif text == "!ctf clear":
        message.is_blocked = True
        furni_list.clear()
        ext.send_to_client('{l}{h:'+SPEECH_IN+'}{i:0}{s:"'+COLOR_ERROR+' Furni list clear !"}{i:0}{i:34}{i:0}{i:0}')

    elif text.startswith("!ctf coord "):
        message.is_blocked = True
        text = text[11:]
        coord = text.split(';')
        x, y = coord
        ext.send_to_client('{l}{h:'+SPEECH_IN+'}{i:0}{s:"'+COLOR_IN+' Coord set to : '+x+' ; '+y+'"}{i:0}{i:34}{i:0}{i:0}')


def furni(message):
    global furni_list
    global wait_id

    (furni_id, _) = message.packet.read('ii')

    if wait_id:
        message.is_blocked = True
        if furni_id not in furni_list:
            furni_list.append(furni_id)
            ext.send_to_client('{l}{h:'+SPEECH_IN+'}{i:0}{s:"'+COLOR_OUT+' Id set to : '+str(furni_id)+'"}{i:0}{i:34}{i:0}{i:0}')
            wait_id = False
        else:
            ext.send_to_client('{l}{h:'+SPEECH_IN+'}{i:0}{s:"'+COLOR_ERROR+' Already saved"}{i:0}{i:34}{i:0}{i:0}')


def clear(message):
    global furni_list
    global wait_id
    global x, y
    wait_id = False
    furni_list.clear()
    x = 0
    y = 0


ext.intercept(Direction.TO_CLIENT, update_furni, FURNI_UPDATE)
ext.intercept(Direction.TO_SERVER, speech, SPEECH_OUT)
ext.intercept(Direction.TO_SERVER, furni, SET_ID)
ext.intercept(Direction.TO_SERVER, clear, CLEAR_LIST)

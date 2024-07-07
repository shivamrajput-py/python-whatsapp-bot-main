import logging
from flask import current_app, jsonify
import json
import requests
from app.utils.data_files.data import *
import re

#------------------------------ !!!! IMPORTANT FUNCTION !!!! NO NEED TO CHANGE ANYTHING HERE -------------------------------------------------------


def process_text_for_whatsapp(text):
    pattern = r"\【.*?\】" # Remove brackets
    text = re.sub(pattern, "", text).strip() # Substitute the pattern with an empty string
    pattern = r"\*\*(.*?)\*\*"  # Pattern to find double asterisks including the word(s) in between
    replacement = r"*\1*" # Replacement pattern with single asterisks
    whatsapp_style_text = re.sub(pattern, replacement, text) # Substitute occurrences of the pattern with the replacement

    return whatsapp_style_text

def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")

def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url,
            data=data,
            headers=headers,
            timeout=10 # 10 seconds timeout as an example
        )

        # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()

    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408

    except (requests.RequestException) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500

    else:
        # Process the response as normal
        log_http_response(response)
        return response


def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )

#------------------------------ !!!! IMPORTANT FUNCTION !!!! NO NEED TO CHANGE ANYTHING HERE -------------------------------------------------------



#--------------------------------- !!! MAIN CODE, THIS IS WHERE WE HAVE TO WORK AND CHANGE !!! -------------------------------------------------------


def find(SUBC: str, TYPE: str ) -> dict:
    # TODO: FINDING MORE SUBJECT CODE GROUPS AND ADDING THEM INTO THIS
    SUBJECT_GROUP_STR = [" CO101 | CO102 | CO116 | CO105 ", ]

    for sub_grp in SUBJECT_GROUP_STR:
        if SUBC in sub_grp:
            SUBC = sub_grp

    with open(r'./app/utils/data_files/Data.json', 'r') as fl:
        doc = json.load(fl)

    if SUBC in doc[0][TYPE].keys():
        return doc[0][TYPE][SUBC]
    else:
        return False

def generate_response(response):
    response: str = response.lower()

    if '/pyq' in response:
        SUBC: str = response.replace('/pyq', '').replace(' ', '')
        if len(SUBC)<2: return "You haven't given the subject code in command!\nPlease Write the command like\n\n/pyq SUBJECT_CODE\n\nexample /pyq AM101\nin this way i will be able to provide you every available PYQ of AM101"
        else:
            req_doc = find(SUBC.upper(), 'PYQ')
            if req_doc == False:
                return f"for the SUBJECT CODE {SUBC}\n\nSorry either you are writing wrong subject code or I dont have any pyq of this specific subject code, SORRY!\n\nContact for feedback and suggestion @shi_kun"
            else:
                req_str: str= ''
                for name in req_doc.keys():
                    if (req_doc[name]!=''):
                        req_str+= f'\n>> *{name}*:\n~{req_doc[name]}\n\n'

                return f"*I have found PYQ's of {SUBC} and here it is:*\n{req_str}"

    elif '/notes' in response:
        SUBC: str = response.replace('/notes', '').strip()
        if len(SUBC) < 2:
            return "You haven't given the subject code in command!\nPlease Write the command like\n\n/notes SUBJECT_CODE\n\nexample /notes AM101\nin this way i will be able to provide you every available notes of AM101"
        else:
            req_doc = find(SUBC.upper(), 'NOTES')
            if req_doc == False:
                return "for the SUBJECT CODE {subjectcode}\n\nSorry either you are writing wrong subject code or I dont have any notes of this specific subject code, SORRY!\n\nContact for feedback and suggestion @shi_kun"
            else:
                req_str: str = ''
                for name in req_doc.keys():
                    if (req_doc[name] != ''): req_str += f'\n>> {name} : LINK: {req_doc[name]}\n'
                return f"I have found NOTES of {SUBC} and here it is:\n{req_str}"

    elif '/assignments' in response:
        SUBC: str = response.replace('/assignments', '').strip()
        if len(SUBC) < 2:
            return "You haven't given the subject code in command!\nPlease Write the command like\n\n/assignments SUBJECT_CODE\n\nexample /assignments AM101\nin this way i will be able to provide you every available Assignments of AM101"
        else:
            req_doc = find(SUBC.upper(), 'ASSIGNMENTS')
            if req_doc == False:
                return "for the SUBJECT CODE {subjectcode}\n\nSorry either you are writing wrong subject code or I dont have any Assignments of this specific subject code, SORRY!\n\nContact for feedback and suggestion @shi_kun"
            else:
                req_str: str = ''
                for name in req_doc.keys():
                    if (req_doc[name] != ''): req_str += f'\n>> {name} : LINK: {req_doc[name]}\n'
                return f"I have found ASSIGNMENTS of {SUBC} and here it is:\n{req_str}"

    elif '/playlists' in response:
        SUBC: str = response.replace('/playlists', '').strip()
        if len(SUBC) < 2:
            return "You haven't given the subject code in command!\nPlease Write the command like\n\n/playlists SUBJECT_CODE\n\nexample /playlists AM101\nin this way i will be able to provide you every available Course Playlist of AM101"
        else:
            req_doc = find(SUBC.upper(), 'PLAYLISTS')
            if req_doc == False:
                return "for the SUBJECT CODE {subjectcode}\n\nSorry either you are writing wrong subject code or I dont have any Playlist of this specific subject code, SORRY!\n\nContact for feedback and suggestion @shi_kun"
            else:
                req_str: str = ''
                for name in req_doc.keys():
                    if (req_doc[name] != ''): req_str += f'\n>> {name} : LINK: {req_doc[name]}\n'
                return f"I have found Course Playlist of {SUBC} and here it is:\n{req_str}"

    elif '/books' in response:
        SUBC: str = response.replace('/books', '').strip()
        if len(SUBC) < 2:
            return "You haven't given the subject code in command!\nPlease Write the command like\n\n/books SUBJECT_CODE\n\nexample /books AM101\nin this way i will be able to provide you every available Books of AM101"
        else:
            req_doc = find(SUBC.upper(), 'BOOKS')
            if req_doc == False:
                return "for the SUBJECT CODE {subjectcode}\n\nSorry either you are writing wrong subject code or I dont have any Books of this specific subject code, SORRY!\n\nContact for feedback and suggestion @shi_kun"
            else:
                req_str: str = ''
                for name in req_doc.keys():
                    if (req_doc[name] != ''): req_str += f'\n>> {name} : LINK: {req_doc[name]}\n'
                return f"I have found Books of {SUBC} and here it is:\n{req_str}"

    elif '/dtu_event' in response:
        return "This feature is currently unavailable, soon i will add this, GIVE US TIME"

    elif '/dtu_notice' in response:
        return "This feature is currently unavailable, soon i will add this, GIVE US TIME"

    elif '/hello' == response:
        return 'Hello There, welcome to DTU Help, use /help to get info'

    elif '/bot_update' in response:
        return 'Shivam here, its been only 4 days since i started working on this, I am adding resources slowly slowly it will take time, i hope you guys understand, Main code part of bot is done, adding more fun stuff soon...'

    elif '/help' in response:
        return HELP_TEXT

    elif 'REP:' in response:
        return response.replace('REP:', '')

    elif 'test' in response:
        data = get_button_link_message_data(current_app.config["RECIPIENT_WAID"], "", "")
        send_message(data)
        return ""

    for greet in GREETINGS_AND_CONVO_DATA:
        if (greet[0] in response) and not (len(response) > len(greet[0]) + 10):
            return greet[1]

    for badword in ABUSES_AND_NEGATIVITY:
        if badword in response:
            return f"Aap {badword} ☺️, Please do not use abusive language 😌"

    return 'Sorry I can not understand what you are trying to say i am still on development phase.'


# -----------------------------!!!  MESSAGE FORMATTING WHATSAPP JSON DIFFERENT MESSAGE FORMATTING !!!---------------------------------------------------------------------------------------------

def get_text_message_data(recipient, text, preview_url: bool =False):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {
                "preview_url": preview_url,
                "body": text
            },
        }
    )

def get_button_link_message_data(recipient, body_text:str, url:str):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "button",
            "sub_type": "quick_reply",
            "index": 0,
            "parameters":
                [{
                    "type": "payload",
                    "payload": "Yes-Button-Payload"
                }]
        }
    )

def get_document_sharing_data(recipient, doc_link, doc_capt: str = "", provider_name: str = ""):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "document",
            "document": {
                "link": doc_link,
                "caption": doc_capt,
                "provider": {
                    "name": provider_name
                }
            }
        }
    )

#------------------------------------------------------------------------------------------------------------------------

# TODO: THE FUMCTION WHICH RECEIVES THE USER RESPONSE AND GIVES IT TO GENERATE RESPONSE FUNCTION
def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"] # Message received from the user

    response = generate_response(message_body) # GENERATE RESPONSE IS THE FUNCTION WHERE ALL OUR WORK LIES

    if response!= '':
        data = get_text_message_data(current_app.config["RECIPIENT_WAID"], response, preview_url=False)
        send_message(data)

#------------------------------------------------------------------------------------------------------------------------

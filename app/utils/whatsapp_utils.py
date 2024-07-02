import logging
from flask import current_app, jsonify
import json
import requests
from data import greeting_all,abuses_negativity
import re

# MAIN CODE ---------------------------------------------------------------------------------------------------------

BOTNAME = 'DTU Help'
BOTUSERNAME = ''
help_text = f"""
    Hello, 
THIS IS {BOTNAME}, And Here is the command list, commands which you can use to make the fulluse of this bot.

/hello -For Greeting, Knowing the bot
/help -This Command which brought you up here
/bot_update - To get latest updates from the bot
/pyq SUBJECT_CODE - get access to PYQ of that subject.
/available_pyq - Get List of all available PYQ
/notes SUBJECT_CODE -get access to All notes related to a subject.
/available_notes - Get List of all available NOTES
/dtu_events - Latest info about Upcoming events in DTU.
/dtu_notices - latest Notices from DTU official website.
/assignments [SUBJECT_CODE] - to access Assignments of that subject.
/books [SUBJECT_CODE] - to access books of that subject.
/playlists [SUBJECT_CODE] - to access course playlists of that subject.
/available_assignment - Get List of all available ASSIGNMENTS
/available_playlist - Get List of all available COURSE PLAYLISTS
/available_books - Get List of all available BOOKS

THIS IS ALL WE GOT FOR NOW! WE ARE ADDING MORE FUNCTIONALITIES, IT WILL TAKE TIME AND YOUR SUPPORT.\nThank You.
    """

def find(SUBC: str, TYPE: str ) -> dict:
    # TODO: FINDING MORE SUBJECT CODE GROUPS AND ADDING THEM INTO THIS
    SUBJECT_GROUP_STR = [" CO101 | CO102 | CO116 | CO105 ", ]

    for sub_grp in SUBJECT_GROUP_STR:
        if SUBC in sub_grp:
            SUBC = sub_grp

    with open(r'Data.json', 'r') as fl:
        doc = json.load(fl)

    if SUBC in doc[0][TYPE].keys():
        return doc[0][TYPE][SUBC]
    else:
        return False

def generate_response(response):
    response: str = response.lower()

    if '/available_pyq' in response:
        with open(r'Data.json', 'r') as fl:
            doc = json.load(fl)
        result_str: str = ''
        for subcode in doc[0]['PYQ'].keys():

            midsems, endsems = [], []
            table_arr: list = [midsems, endsems]

            # SEPARATING MIDSEM AND ENDSEM NAMES ON DIFFERENT LIST
            for pyq_ in doc[0]['PYQ'][subcode].keys():
                if (doc[0]['PYQ'][subcode][pyq_] != "" and 'MID' in pyq_):
                    midsems.append(pyq_)
                elif doc[0]['PYQ'][subcode][pyq_] != "" and 'END' in pyq_:
                    endsems.append(pyq_)
                elif doc[0]['PYQ'][subcode][pyq_] != "":
                    midsems.append(pyq_)

            len_mid = len(midsems)
            len_end = len(endsems)

            if len_mid + len_end != 0:

                result_str += f'\n\nFOR SUBJECT: {subcode} I HAVE PYQS OF\n'

                # CHECKING WHICH LIST IS SMALLER SO THAT WE HAVE TO FILL EMPTY ELEMENTS OF IT.
                if len_mid >= len_end:
                    lenn = [len_mid, 'e']
                else:
                    lenn = [len_end, 'm']

                j = 1
                for i in range(0, lenn[0]):

                    if ((lenn[1] == 'e') and ((i + 1) > len_end)):
                        result_str += f'\n        {table_arr[0][i]}        |        {len(table_arr[1][i - j]) * '_'}        '
                        j += 1

                    elif ((lenn[1] == 'm') and ((i + 1) > len_mid)):
                        result_str += f'\n        {len(table_arr[0][i - j]) * '_'}        |        {table_arr[1][i]}        '
                        j += 1

                    else:
                        result_str += f'\n        {table_arr[0][i]}        |        {table_arr[1][i]}        '

                # return (f'{result_str}')
            else:
                pass

        return result_str
        # return (f'Adding more subjects... GIVE US TIME, still on development phase')

    elif '/pyq' in response:
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
                        data = get_button_link_message_input(current_app.config["RECIPIENT_WAID"], name, req_doc[name])
                        send_message(data)



                    # if (req_doc[name]!=''): req_str+= f'\n>> {name} : LINK: {req_doc[name]}\n'
                # return f"I have found PYQ's of {SUBC} and here it is:\n{req_str}"

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
        return help_text

    for greet in greeting_all:
        if (greet[0] in response) and not (len(response) > len(greet[0]) + 10):
            return greet[1]

    for badword in abuses_negativity:
        if badword in response:
            return f"Aap {badword} ☺️, Please do not use abusive language 😌"

    return 'Sorry I can not understand what you are trying to say i am still on development phase.'

# --------------------------------------------------------------------------------------------------------------------------

def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        })


def get_button_link_message_input(recipient, body_text:str, url:str):
    return json.dumps(
        # {
        #     "messaging_product": "whatsapp",
        #     "preview_url": True,
        #     "recipient_type": "individual",
        #     "to": recipient,
        #     "type": "document",
        #     "document": {
        #         "link": url,
        #         "provider": {
        #             "name" : body_text
        #         }
        #     }
        # }

        {
            "messaging_product": "whatsapp",
            "preview_url": True,
            "recipient_type": "individual",
            "to": recipient,
            "type":"text",
            "text":{
                "body": f'{url}'
            }

        }
    )


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response


def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text


def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]

    # TODO: implement custom function here
    response = generate_response(message_body)

    data = get_text_message_input(current_app.config["RECIPIENT_WAID"], response)
    send_message(data)


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


from json import dumps
from config import g_chat_url, BASE_DATA_PATH, email_creds
from httplib2 import Http
import smtplib


def send_to_g_chat(data):
    url = g_chat_url["G_CHAT_URL"]
    if len(str(data)) >= 4096:

        # email creds
        email = email_creds["email"]
        password = email_creds["password"]
        send_to_email = email_creds["send_to_email"]
        subject = 'ym reply payload'

        # cresting a file
        with open(f"{BASE_DATA_PATH}/ym_replies.txt", "w") as reply:
            reply.write(str(data))
        file_location = f"{BASE_DATA_PATH}/ym_replies.txt"
        with open(file_location) as f:
            message = f.read()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        text = "Subject: {}\n\n{}".format(subject, message)
        server.sendmail(email, send_to_email, text)
        server.quit()

    else:
        bot_message = {
            'text': str(data)}
        bot_message = dumps(bot_message)
        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
        http_obj = Http()
        response = http_obj.request(
            uri=url,
            method='POST',
            headers=message_headers,
            body=bot_message,
        )

    return "message has sent"


if __name__ == '__main__':
    res = send_to_g_chat(data="hello")
    print(res)

from revChatGPT.V1 import Chatbot
from pprint import pprint

email = '<your_email>'
password = '<your_password>'

configs = {'email':email, 'password':password}
bot = Chatbot(config = configs)


def clean_text(text):

    text = text.replace('\n','')
    text = text.replace("'\'",'')

    return text

prompt = input('Ask Question : ')
response = ''

try:
    for data in bot.ask(prompt):
        response = clean_text(str(data['message']))
except:
    pass

data = dict()
data['Question'] = prompt
data['Answer'] = response

pprint(data)

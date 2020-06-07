from flask import Flask
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")

@app.route('/')
def homepage():
    return "Hi there, how ya doin?"


@ask.launch
def start_skill():
    welcome_message = 'Oi, bem vindo ao aplicativo Vida Boa. Você gostaria de iniciar?'
    return question(welcome_message)

@ask.intent("AMAZON.YesIntent")
def share_headlines():
    headlines = 'Vida Boa'
    headline_msg = 'Legal. Você iniciou a rotina de {}. Você gostaria de ouvir alguma receita, ou para sair dessa skill, diga parar.'.format(headlines)
    return question(headline_msg)

@ask.intent("UserResponseIntent")
def share_headlines(comida):
    print("Coletando receita de {}".format(comida))
    headlines = 'Aqui vai uma receita de {}. Bota tudo no forno. E agora, o que você gostaria de fazer?'.format(comida)
    headline_msg = headlines
    return question(headline_msg)


@ask.intent("AMAZON.NoIntent")
def no_intent():
    bye_text = 'Ok, tenha uma boa semana e fique em casa.'
    return statement(bye_text)


if __name__ == '__main__':
    app.run(debug=True)

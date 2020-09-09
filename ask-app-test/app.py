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
    reprompt_msg = "Fale sim, se gostaria de iniciar, ou não, caso queira sair."
    session.attributes['route'] = ['Inicio']
    print(session.attributes['route'])
    return question(welcome_message).reprompt(reprompt_msg)

@ask.intent("AMAZON.NavigateHomeIntent")
def home():
    session.attributes['route'] += ['Home']
    print(session.attributes['route'])
    
    headlines = 'Vida Boa'
    headline_msg = 'Legal. Você iniciou a rotina de {}. Você gostaria de ouvir alguma receita, ou para sair dessa skill, diga parar.'.format(headlines)
    return question(headline_msg)
    

@ask.intent("AMAZON.YesIntent")
def yes_intent():
    session.attributes['route'] += ['Sim']
    print(session.attributes['route'])
    
    return home()

@ask.intent("UserResponseIntent")
def share_headlines(comida):
    session.attributes['route'] += [{'Receita': comida}]
    print(session.attributes['route'])
    
    
    print("Coletando receita de {}".format(comida))
    pre_msg = ""

    if 'chosen_food' in session.attributes.keys():
        last_choice = session.attributes['chosen_food']
        print("Last Choice {}".format(last_choice))
        if last_choice is not None:
            pre_msg = "Sua última escolha foi {}".format(last_choice)
    session.attributes['chosen_food'] = comida
    headlines = '{}. Aqui vai uma receita de {}. Bota tudo no forno. E agora, o que você gostaria de fazer?'.format(pre_msg, comida)
    headline_msg = headlines
    return statement("Ah").simple_card(title="Receita de {}".format(comida), content="Bota no forno.") + question(headline_msg)


@ask.intent("AMAZON.NoIntent")
def no_intent():
    session.attributes['route'] += ['Nao']
    print(session.attributes['route'])
    
    bye_text = 'Ok, tenha uma boa semana e fique em casa.'
    return statement(bye_text)

@ask.intent("AMAZON.StopIntent")
def no_intent():
    session.attributes['route'] += ['Saindo']
    print(session.attributes['route'])
    
    bye_text = 'Ok, tenha uma boa semana e fique em casa.'
    return statement(bye_text)



if __name__ == '__main__':
    app.run(debug=True)

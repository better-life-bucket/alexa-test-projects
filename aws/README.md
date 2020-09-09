Nunca mais se esqueça de onde você deixou o seu celular, ou suas chaves. A skill Localizador de Objetos te ajuda a encontrar suas coisas espalhadas pela casa.

Comece ativando a skill na sua conta e falando "Alexa, abrir localizador de objetos" para abri-la.

Registre seus objetos e sua localização, por exemplo, ao colocar suas chaves em cima da mesa, você pode dizer para a skill "Minha chave está em cima da mesa" ou "Coloquei a chave em cima da mesa".

Para localizar seus objetos registrados, você pode dizer para a skill "Onde está minha chave?" ou "Localizar chave" e, após algumas confirmações, o localizador de objetos irá te lembrar onde você colocou suas chaves pela última vez.

Tente também localizar seus objetos com uma única frase, por exemplo, com a skill fechada, você pode dizer "Alexa, onde está minha chave no localizador de objetos?".

Essa skill tem por objetivo maior acessibilidade para pessoas que tem dificuldade de se lembrar onde suas coisas estão guardadas.




Testes:

Skill is in portuguese only. It uses your Alexa user id as key to store the objects and their locations in order to retrieve in a new session.
Test0 - Open skill - Say 'Alexa, abrir localizador de objetos'
-> It should respond with an welcoming message
Test1: First access - With opened skill, try retrieve any object location by saying "Onde está meu celular?"
-> It should tell you to start storing object's location first
Test2: Store Object - With opened skill, try store any object location by saying "Coloquei meu celular em cima da mesa?"
-> It should ask for confirmation about the object "celular" and location "em cima da mesa". If you confirme by saying 'Sim' for both, it will register the location of this object.
Test3: Retrieve existing objects location - Repeat Test1.
-> Now it should ask for confirmation about objects name "celular". If you confirm by saying 'Sim', it should tell you the location of this object "Eu encontrei 'celular'. 'Celular' está 'em cima da mesa'".
Test3: Retrieve non-existing objects location - With opened skill, try retrieve any non stored object location by saying "Onde está minha carteira?".
-> Now it should ask for confirmation about objects name "carteira". If you confirm by saying 'Sim', it should tell you that this object could not be located "Eu não encontrei 'carteira'. And also will tell you to, once you find the object you could store it and next time the skill will remember its location.

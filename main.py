from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ListTrainer
from flask import Flask, render_template, request, make_response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/jarvis": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


DEFAULT_ANSWER = "I'm just 3 days old right now and I haven't grasped your language that well but I'm trying! 😉"

bot = ChatBot(
    "jarvis",
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch',
    ],
)

trainer = ListTrainer(bot)

# trainer.train("chatterbot.corpus.english.greetings")

dataCollection = []
with open('topical_chat.csv', encoding='utf-8') as trainingData:
    for line in trainingData:
        dataSet = line.split(",")
        dataCollection.append(dataSet[1])
        # dataCollection.append(dataSet[2])

print(len(dataCollection))
trainer.train(dataCollection)


def processData(data):
    result = bot.generate_response(Statement(data))
    if len(result.text) == 1:
        return DEFAULT_ANSWER
    return result.text


@app.route('/')
@cross_origin()
def hello_world():
    return render_template('index.html')


@app.route('/jarvis', methods=["GET", "POST"])
@cross_origin()
def jarvis():
    if request.method == 'GET':
        print(request)
        return make_response({"response": "Hello, this is an invalid request!"})
    elif request.method == 'POST':
        try:
            return make_response({"response": processData(request.data.decode('utf-8')[9:-2])})
        except Exception as e:
            return make_response({"error": repr(e)})


if __name__ == '__main__':
    app.run()


from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
from studchat import generate_response
import teachbot 
import guest

app = Flask(__name__)
app.secret_key = 'your_secret_key'
client = MongoClient('mongodb://localhost:27017/')  # MongoDB connection
db = client['miniprojusers']  # Database name
collection = db['users']  # Collection name

@app.route('/')
def home():
    return render_template('login.html')



@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = collection.find_one({'username': username, 'password': password})
    if user:
        query = {'username': username, 'password': password}
        type = collection.find_one(query, {"type": 1})
        uid = collection.find_one(query, {"id":1})
        user_type = type["type"]
        user_id = uid["id"]

        session['uid'] = user_id
        session['type'] = user_type
        session['username'] = username
        session['logged_in'] = True
        
        return redirect('/val')
    else:
        return render_template('login.html', error='Invalid credentials')




@app.route('/val')
def validate():
    if not session.get('logged_in'):
        return redirect('/')
    usrnm = session['username'].title()
    return render_template('index.html',usrnm=usrnm)

@app.route('/guest')
def redir():
    return render_template('index1.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return redirect('/')



@app.route('/reg', methods=['GET'])
def new_user():
    return render_template('register.html')



@app.route('/reg', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    uid = request.form['uid']

    existing_user = collection.find_one({'username': username})
    if existing_user:
        return render_template('register.html', error='Username already exists')

    user = {
        'username': username,
        'password': password,
        'type': '0',
        'id' : uid
    }
    collection.insert_one(user)

    session['logged_in'] = True
    session['username'] = username
    usrnm = session['username'].title()
    return render_template('index.html',usrnm=usrnm)


@app.route('/chat', methods=['POST'])
def chat():
    tp = int(session['type'])
    uid = session['uid']
    if not session.get('logged_in'):
        return redirect('/')
    elif tp == 1 :
        usrnm = session['username'].title()
        user_input = request.form['user_input']
        query= user_input
        processed_input = teachbot.preprocess_text(user_input)
        response = teachbot.bot.get_response(processed_input)
        respconf = response.confidence
        if respconf >= 0.4:
            return render_template('index.html', user_input=user_input, response=response, usrnm=usrnm, respconf=respconf, query=query)
        else:
            return render_template('index.html', user_input=user_input, response="Sorry, I didnt understand.", usrnm=usrnm, respconf=respconf, query=query)
    elif tp==0  :
        usrnm = session['username'].title()
        user_input = request.form['user_input']
        querys= user_input
        response = generate_response(uid,user_input)
        if response is not None:
            return render_template('index.html', user_input=user_input, response=response, usrnm=usrnm, query=querys)
        else:
            return render_template('index.html', user_input=user_input, response="Sorry, I didnt understand.", usrnm=usrnm, query=querys)
    else :
        return render_template('index.html', user_input=user_input, response="Sorry, I didnt understand.", usrnm=usrnm, query=querys)
    

@app.route('/chat1', methods=['POST'])
def chat1():
    user_input = request.form['user_input']
    query= user_input
    response = guest.bot.get_response(user_input)
    respconf = response.confidence
    if respconf >= 0.4:
        return render_template('index1.html', user_input=user_input, response=response, respconf=respconf, query=query)
    else:
        return render_template('index1.html', user_input=user_input, response="Sorry, I didnt understand.", respconf=respconf, query=query)


@app.route('/goback', methods=['POST'])
def goback():
    return redirect('/')


if __name__ == '__main__':
    app.run()

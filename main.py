from flask import Flask, render_template, request, jsonify
import json
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shreyas'
socketio = SocketIO(app)
loggedInUser = ''

# @app.route('/')
# def sessions():
#     return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)
    
# @socketio.on('my event')
# def handle_my_custom_event(json, methods=['GET', 'POST'])
#     print('received my event: ' + str(json))
#     socketio.emit('my response', json, callback=messageReceived)


@app.route('/')
def login():
  return render_template('login.html')

@app.route('/about/')
def about():
    if (loggedInUser == ''):
        return render_template('login.html')
    return render_template('about.html') 

@app.route('/home/')
def home():
    if (loggedInUser == ''):
        return render_template('login.html')
    return render_template('home.html')


@app.route('/location/')
def location():
    if (loggedInUser == ''):
        return render_template('login.html')
    return render_template('location.html')

@app.route('/FAQs/')
def FAQs():
    if (loggedInUser == ''):
        return render_template('login.html')
    return render_template('FAQs.html')

@app.route('/chat/')
def chat():
    if (loggedInUser == ''):
        return render_template('login.html')

    return render_template('chat.html')

@app.route('/your_flask_funtion')
def get_ses():
	"make your needs here"


@app.route('/pushData',  methods=['POST'])
def getData():
    global loggedInUser
    if request.method == "POST":
      loggedInUser = request.get_json()
      print(loggedInUser)

    return jsonify()

@app.route('/PatientDetails/', methods=['POST', 'GET'])
def PatientDetails():
    if (loggedInUser == ''):
        return render_template('login.html')
  
    print(loggedInUser)
    isAdmin = False
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "data.json")
    data = json.load(open(json_url))
    output_json = json.dumps(data)
    json_object= json.loads(output_json)
  
    if "admin" == loggedInUser.lower():
        isAdmin = True

    print("filtering")
    if request.method == 'POST':
        strTextBoxVal = request.form['searchInput']
        output_dict = [x for x in data if x['area'] == strTextBoxVal.lower()]
        output_json = json.dumps(output_dict)
        json_object = json.loads(output_json)
        print(json_object)
        print(type(json_object))
        
    return render_template('PatientDetails.html', rows=json_object, role=isAdmin)
if __name__ == '__main__':
   port = os.environ.get("PORT",5000)
   app.run(port=port,host = "0.0.0.0",debug=True)
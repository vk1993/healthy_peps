from flask import Flask, render_template,request
import urllib.request 
import json
from flask import Flask, render_template
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shreyas'
socketio = SocketIO(app)

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
    return render_template('about.html') 

@app.route('/home/')
def home():
    return render_template('home.html')


@app.route('/location/')
def location():
    return render_template('location.html')

@app.route('/FAQs/')
def FAQs():
    return render_template('FAQs.html')

@app.route('/chat/')
def chat():
    return render_template('chat.html')

@app.route('/your_flask_funtion')
def get_ses():
	"make your needs here"

@app.route('/PatientDetails/', methods=['POST', 'GET'])
def PatientDetails():
  SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
  json_url = os.path.join(SITE_ROOT, "static/data", "data.json")
  data = json.load(open(json_url))
  output_json = json.dumps(data)
  json_object= json.loads(output_json)
  print("filtering")
  if request.method == 'POST':
    strTextBoxVal = request.form['searchInput']
    output_dict = [x for x in data if x['area'] == strTextBoxVal.lower()]
    output_json = json.dumps(output_dict)
    json_object = json.loads(output_json)
    print(json_object)
    print(type(json_object))
    
  return render_template('PatientDetails.html', rows=json_object)
if __name__ == '__main__':
   app.run(port=5005,debug=True)
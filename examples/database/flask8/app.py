from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect
import MySQLdb       
import math
import time
import configparser
import random

async_mode = None

app = Flask(__name__)


config = configparser.ConfigParser()
config.read('config.cfg')
myhost = config.get('mysqlDB', 'host')
myuser = config.get('mysqlDB', 'user')
mypasswd = config.get('mysqlDB', 'passwd')
mydb = config.get('mysqlDB', 'db')
print(myhost)


app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock() 


def background_thread(args):
    count = 0
    init_time = time.time()
    dataCounter = 0 
    dataList = []  
    db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)


    while True:
        if args:
          A = dict(args).get('A')
          dbV = dict(args).get('db_value')
        else:
          A = 1
          dbV = 'nieco'

        #print(A
        #print(dbV 
        print(args )
        socketio.sleep(1)
        count += 1
        dataCounter +=1
        prem = random.random()

        seconds = time.time() - init_time
        seconds = seconds *20;

        if seconds > 360:
            init_time = time.time()

        if dbV == 'start':
          dataDict = {
            "t": time.time(),
            "x": dataCounter,
            "sin": float(A)*math.sin(math.radians(seconds)),
            "cos": float(A)*math.cos(math.radians(seconds))
          }
          dataList.append(dataDict)
        else:
          if len(dataList)>0:
            print((str(dataList)))
            fuj = str(dataList).replace("'", "\"")
            print(fuj)
            # cursor = db.cursor()
            # cursor.execute("SELECT MAX(id) FROM graph")
            # maxid = cursor.fetchone()
            # cursor.execute("INSERT INTO graph (id, hodnoty) VALUES (%s, %s)", (maxid[0] + 1, fuj))
            # db.commit()

            fo = open("static/files/test.txt", "a+")
            fo.write("%s\r\n" % fuj)

          dataList = []
          dataCounter = 0


        # socketio.emit('my_response',
        #               {'data': float(A)*prem, 'count': count},
        #               namespace='/test')

        socketio.emit('my_response',
                      {'data': float(A)*math.sin(math.radians(seconds)),
                       'cos':   float(A)*math.cos(math.radians(seconds)), 'count': count},
                      namespace='/test')

    db.close()

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    return render_template('graph.html', async_mode=socketio.async_mode)
    
@app.route('/db')
def db():
  db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
  cursor = db.cursor()
  cursor.execute('''SELECT  hodnoty FROM  graph WHERE id=1''')
  rv = cursor.fetchall()
  return str(rv)    

@app.route('/dbdata/<string:num>', methods=['GET', 'POST'])
def dbdata(num):
  # db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
  # cursor = db.cursor()
  # print(num)
  # cursor.execute("SELECT hodnoty FROM  graph WHERE id=%s", num)
  # rv = cursor.fetchone()

  fo = open("static/files/test.txt", "r")
  rows = fo.readlines()
  return rows[int(num) - 1]

    
@socketio.on('db_id_event', namespace='/test')
def change_database(message):
    # session['receive_count'] = session.get('receive_count', 0) + 1
    # session['A'] = message['value']
    # emit('my_response',
    #      {'data': message['value'], 'count': session['receive_count']})
    print("Chosed database\n")
    print(message['value'])

@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    session['A'] = message['value']
    emit('my_response',
         {'data': message['value'], 'count': session['receive_count']})

@socketio.on('db_event', namespace='/test')
def db_message(message):   
#    session['receive_count'] = session.get('receive_count', 0) + 1 
    session['db_value'] = message['value']    
#    emit('my_response',
#         {'data': message['value'], 'count': session['receive_count']})

@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
   # emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)

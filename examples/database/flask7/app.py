from flask import Flask, render_template
import MySQLdb       
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.cfg')
myhost = config.get('mysqlDB', 'host')
myuser = config.get('mysqlDB', 'user')
mypasswd = config.get('mysqlDB', 'passwd')
mydb = config.get('mysqlDB', 'db')
print(myhost)


@app.route('/')
def index():
    return "hello"

@app.route('/dbadd/<string:insert>')
def add(insert):
  db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
  cursor = db.cursor()
  cursor.execute("SELECT MAX(id) FROM prva")
  maxid = cursor.fetchone() 
  print(maxid[0]+1)
  print(insert)
  cursor.execute("INSERT INTO prva (id, popis) VALUES (%s,%s)",(maxid[0]+1,insert))
  db.commit()
  return "Done"

@app.route('/dbdata/<int:num>', methods=['GET', 'POST'])
def dbdata(num):
  db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
  cursor = db.cursor()
  print(num)
  cursor.execute("SELECT popis FROM prva WHERE id=%i" % (num))
  rv = cursor.fetchone()
  print(rv)
  return str(rv[0])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)

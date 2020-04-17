from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return "hello"

#  "a" - Append - will append to the end of the file
#  "w" - Write - will overwrite any existing content
#  "r" - Read - will read the content of the file
# pri zapise do suboru musia byt na nadradenom adresari nastavene prava na zapis do adresaru

@app.route('/write')
def write2file():
    fo = open("static/files/test.txt","a+")    
    val = '[{"y": 0.6551787400492523, "x": 1, "t": 1522016547.531831}, {"y": 0.47491473008127605, "x": 2, "t": 1522016549.534749}, {"y": 0.7495528524284468, "x": 3, "t": 1522016551.537547}, {"y": 0.19625207463282368, "x": 4, "t": 1522016553.540447}, {"y": 0.3741884249440639, "x": 5, "t": 1522016555.543216}, {"y": 0.06684808042190538, "x": 6, "t": 1522016557.546104}, {"y": 0.17399442194131343, "x": 7, "t": 1522016559.54899}, {"y": 0.025055174467733865, "x": 8, "t": 1522016561.551384}]'
    fo.write("%s\r\n" %val)
    return "done"

@app.route('/read/<string:num>')
def readmyfile(num):
    fo = open("static/files/test.txt","r")
    rows = fo.readlines()
    return rows[int(num)-1]

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    return render_template('graph.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)

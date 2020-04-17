from flask import Flask, render_template

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def hello():
    return "Hello word!"

@app.route('/hello1')
def hello1():
    return "Ahoj 1"

@app.route('/hello2')
def hello2():
    return render_template('hello2.html')

@app.route('/hello3')
def hello3():
    prem = 7.0543
    user = { 'meno': 'Peter', 'priezvisko': 'Kolek'}
    return render_template('hello3.html', prem=prem, user=user)

@app.route('/hello4/<user>')
def hello4(user):
    return render_template('hello4.html', name=user)    
    



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)

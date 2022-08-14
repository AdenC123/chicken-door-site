from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('Home.html')


@app.route('/open')
def opens():
    print('opening...')
    return render_template('Home.html')


@app.route('/close')
def closes():
    print('closing...')
    return render_template('Home.html')


@app.route('/send_times', methods=['POST'])
def update_times():
    open_time = request.form['open-time']
    close_time = request.form['close-time']
    print(open_time)
    print(close_time)
    return render_template('Home.html')


if __name__ == '__main__':
    app.run(port=5100)

from flask import Flask, render_template, request, url_for, send_file
from main import main

app = Flask(__name__, static_url_path="/static")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plots/<filename>')
def sendPlot(filename):
    return send_file(f'./plots/{filename}.png', mimetype='image/png')

@app.route('/correlations', methods=['GET'])
def correlations():
    if request.method == 'GET':
        tf = request.args.get('tf')
        main(tf)
        return render_template('correlations.html', tf=tf)
        
app.run()

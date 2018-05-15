from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return render_template('dashboard.html')
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.secret_key = os.urandom(24)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=port, debug=True)
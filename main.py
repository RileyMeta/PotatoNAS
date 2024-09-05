from flask import Flask, render_template, redirect, request, jsonify, url_for, Response, session, flash
import matplotlib.pyplot as plt
import io, pam, logging
from logging.handlers import RotatingFileHandler
from functools import wraps
from cpu import *
from disks import *
from dockers import *
from memory import *
from misc import *
from network import *
from virtualmachines import *

VERSION: str = '1.0.0'

app = Flask(__name__)
app.secret_key = '3c9c38390229b7519fa9603376af11c12dbc07dc812ea823b3c8472bfcfd50b5'

pam_auth = pam.pam()

handler = RotatingFileHandler('logs/login_attempts.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

logger.propagate = False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You need to be logged in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/plot.png')
@login_required
def plot_png():
    fig = create_pie_chart()
    output = io.BytesIO()
    fig.savefig(output, format='png')
    output.seek(0)
    return Response(output.getvalue(), mimetype='image/png')

def create_pie_chart():
    max_value = int(get_total_memory())
    dynamic_value = int(get_used_memory())
    remaining_value = max_value - dynamic_value

    sizes = [dynamic_value, remaining_value]
    labels = ['Used', 'Remaining']
    colors = ['#ff9999','#66b3ff']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')

    fig.patch.set_alpha(0)

    return fig

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if pam_auth.authenticate(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            logger.info(f'Failed login attempt: Username: {username}, IP: {request.remote_addr}')
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/")
@login_required
def index():
    return render_template('index.html', page_title="PotatoNAS | Home")

@app.route("/accounts")
@login_required
def accounts():
    return render_template('accounts.html')

@app.route("/system_info")
@login_required
def system_info():
    return render_template('system_info.html')

@app.route("/network_and_shares")
@login_required
def network_and_shares():
    return render_template('network_and_shares.html')

@app.route("/tasks")
@login_required
def tasks():
    return render_template('tasks.html')

@app.route("/virtualmachines")
@login_required
def virtual_machines():
    return render_template('virtualmachines.html')

@app.route("/dockers")
@login_required
def dockers():
    return render_template('dockers.html')

@app.route("/system_settings")
@login_required
def system_settings():
    return render_template('system_settings.html')

@app.route('/shell', methods=['GET', 'POST'])
@login_required
def shell():
    if request.method == 'POST':
        command = request.form.get('command')
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            return jsonify({'output': output})
        except subprocess.CalledProcessError as e:
            return jsonify({'error': e.output})

    return render_template('shell.html')

@app.route("/api_keys")
@login_required
def api_keys():
    return render_template('api_keys.html')

@app.route("/guides")
def guides():
    return render_template('guides.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/copyright")
def copyright():
    return render_template('copyright.html')



if __name__ == '__main__':
    app.run(debug=True)
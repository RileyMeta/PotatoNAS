from flask import Flask, render_template, Response
import subprocess
import matplotlib.pyplot as plt
import io
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/plot.png')
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

    return fig

def get_total_memory():
    result = subprocess.run(['free', '-m'], 
        text=True, 
        capture_output=True,)
    free_output = result.stdout

    mem_line = subprocess.run(
        ['grep', '^Mem:'],
        input=free_output,
        capture_output=True,
        text=True
    ).stdout

    total_memory = subprocess.run(
        ['awk', '{print $2}'],
        input=mem_line,
        capture_output=True,
        text=True
    ).stdout.strip()
 
    return round(int(total_memory) / 1000)

def get_used_memory():
    result = subprocess.run(['free', '-m'], 
        text=True, 
        capture_output=True,)
    free_output = result.stdout

    mem_line = subprocess.run(
        ['grep', '^Mem:'],
        input=free_output,
        capture_output=True,
        text=True
    ).stdout

    used_memory = subprocess.run(
        ['awk', '{print $3}'],
        input=mem_line,
        capture_output=True,
        text=True
    ).stdout.strip()
 
    return round(int(used_memory) / 1000)

def get_memory_usage():
    memory_usage = (int(get_total_memory()) / int(get_used_memory()))

    return round(memory_usage, ndigits=2)



if __name__ == '__main__':
    app.run(debug=True)

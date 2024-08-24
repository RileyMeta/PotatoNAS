import subprocess
from flask import Flask, render_template

app = Flask(__name__)

def get_cpu_model_name():
    result = subprocess.run(['lscpu'], 
        capture_output=True, 
        text=True)
    lscpu_output = result.stdout

    model_name_line = subprocess.run(
        ['grep', 'Model name'],
        input=lscpu_output,
        capture_output=True,
        text=True
    ).stdout

    model_name = subprocess.run(
        ['cut', '-f', '2', '-d', ':'],
        input=model_name_line,
        capture_output=True,
        text=True
    ).stdout

    model_name = subprocess.run(
        ['awk', '{$1=$1}1'],
        input=model_name,
        capture_output=True,
        text=True
    ).stdout.strip()

    return model_name

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

def get_disk_usage(format_type='full'):
    result = subprocess.run(['df', '-T', '/'], capture_output=True, text=True)
    df_output = result.stdout

    # Split the output into lines and columns
    lines = df_output.splitlines()
    if len(lines) > 1:
        headers = lines[0].split()
        values = lines[1].split()
        
        filesystem = values[0]
        fstype = values[1]
        size = values[2]
        used = values[3]
        avail = values[4]
        use_percent = values[5]
        mounted_on = values[6]
        
        match format_type:
            case 'full':
                return {
                    'Filesystem': filesystem,
                    'Type': fstype,
                    'Size': size,
                    'Used': used,
                    'Available': avail,
                    'Use%': use_percent,
                    'Mounted on': mounted_on
                }
            case 'size':
                return round(int(size) / 1000024, ndigits=2)
            case 'used':
                return round(int(used) / 1000024, ndigits=2)
            case 'avail':
                return round(int(avail) / 1000024, ndigits=2)
            case 'use%':
                return use_percent
            case 'fstype':
                return fstype
            case 'mount':
                return mounted_on
            case _:
                return "Invalid format_type argument"

    return "No information available"

def get_hostname():
    filepath = "/etc/hostname"
    try:
        with open(filepath, 'r') as file:
            content = file.read()
        return content.strip()
    except FileNotFoundError:
        return f"File not found: {filepath}"
    except IOError as e:
        return f"An error occurred: {e}"

def get_cpu_load_average():
    with open("/proc/loadavg", "r") as file:
        load_avg = file.read().split()

    # Extracting the 1, 5, and 15 minute load averages
    one_minute_load = load_avg[0]
    five_minute_load = load_avg[1]
    fifteen_minute_load = load_avg[2]

    return one_minute_load

def get_system_uptime():
    result = subprocess.run(['uptime', '-p'], stdout=subprocess.PIPE, text=True)
    uptime = result.stdout.strip().replace('up ', '') # Remove "up"
    return uptime



@app.route("/")
def index():
    return render_template('index.html', 
                            cpu=get_cpu_model_name, 
                            disk_usage=get_disk_usage,
                            get_total_memory=get_total_memory, 
                            get_hostname=get_hostname,
                            get_cpu_load=get_cpu_load_average,
                            get_uptime=get_system_uptime)

if __name__ == '__main__':
    app.run()

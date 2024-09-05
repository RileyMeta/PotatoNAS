import subprocess, socket, psutil, datetime

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

def get_cpu_process():
    result = subprocess.run(['ps', '-e'], stdout=subprocess.PIPE, text=True)
    
    process_count = len(result.stdout.strip().split('\n')) - 1
    
    return process_count

def get_cpu_load_average():
    with open("/proc/loadavg", "r") as file:
        load_avg = file.read().split()

    # Extracting the 1, 5, and 15 minute load averages
    one_minute_load = load_avg[0]
    five_minute_load = load_avg[1]
    fifteen_minute_load = load_avg[2]

    return one_minute_load

def get_boot_time():
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    return boot_time
import subprocess, socket, psutil, speedtest, threading

VERSION = "0.01 Beta"
download_speed = None

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

def get_free_memory():
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

    free_memory = subprocess.run(
        ['awk', '{print $4}'],
        input=mem_line,
        capture_output=True,
        text=True
    ).stdout.strip()
 
    return round(int(free_memory) / 1000)

def get_memory_usage():
    memory_usage = (int(get_total_memory()) / int(get_used_memory()))

    return round(memory_usage, ndigits=2)

def get_disk_usage(format_type='full'):
    path = '/'
    result = subprocess.run(['df', '-T', path], capture_output=True, text=True)
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
            case 'path':
                return path
            case _:
                return "Invalid format_type argument"

    return "No information available"

def get_logs():
    filepath = "/etc/PotatoNAS/logs"
    try:
        with open(filepath, 'r') as file:
            content = file.read()
        return len(content.strip())
    except FileNotFoundError:
        return f"File not found: {filepath}"
    except IOError as e:
        return f"An error occurred: {e}"


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

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()

    return ip_address

def get_active_network_interface():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()

    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET and addr.address == local_ip:
                return interface
    return None

def get_network_interface_type(interface):
    try:
        with open(f"/sys/class/net/{interface}/wireless") as f:
            return "Wi-Fi"
    except FileNotFoundError:
        return "Ethernet"
    return "Unknown"

def get_internet_speed():
    try:
        st = speedtest.Speedtest()
        print("Testing internet speed...")
        download_speed = st.download() / 1000000  # Convert to Mbps
        return round(download_speed, ndigits=2)

    except speedtest.SpeedtestException as e:
        print("An error occurred during the speed test:", str(e))

def get_kernel_version():
    result = subprocess.run(['uname', '-r'], text=True, capture_output=True)
    kernel_version = result.stdout.strip()
    return kernel_version

def get_username():
    result = subprocess.run(['whoami'], text=True, capture_output=True)
    username = result.stdout.strip()
    return username

def speedtest_thread():
    global download_speed
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000

def start_speedtest():
    test_thread = threading.Thread(target=speedtest_thread)
    test_thread.start()
    
    test_thread.join()
    
    return round(download_speed, ndigits=2)

import subprocess, socket, psutil, speedtest, threading, time

VERSION = "0.01 Beta"
download_speed = None

def sleep(int):
    time.sleep(int)

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

# def get_username():
#     result = subprocess.run(['whoami'], text=True, capture_output=True)
#     username = result.stdout.strip()
#     return username

def get_system_uptime():
    result = subprocess.run(['uptime', '-p'], stdout=subprocess.PIPE, text=True)
    uptime = result.stdout.strip().replace('up ', '') # Remove "up"
    return uptime

def get_kernel_version():
    result = subprocess.run(['uname', '-r'], text=True, capture_output=True)
    kernel_version = result.stdout.strip()
    return kernel_version

import subprocess, socket, psutil, speedtest, threading, time

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
        ['awk', '{print $7}'],
        input=mem_line,
        capture_output=True,
        text=True
    ).stdout.strip()
 
    return round(int(free_memory) / 1000)

def get_memory_usage():
    memory_usage = (int(get_total_memory()) / int(get_used_memory()))

    return round(memory_usage, ndigits=2)
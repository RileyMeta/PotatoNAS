import subprocess, socket, psutil, speedtest, threading, time

def get_total_vms():
    result = subprocess.run(['virsh', 'list', '--all'], text=True, capture_output=True)

    total_vms = 0

    for line in result.stdout.splitlines():
        if line.strip() and not line.startswith(" Id") and not line.startswith("-"):
            total_vms += 1

    return total_vms

def get_offline_vms():
    result = subprocess.run(['virsh', 'list', '--all'], text=True, capture_output=True)

    # Filter out VMs that are shut off
    offline_vms = []
    for line in result.stdout.splitlines():
        if 'shut off' in line:
            vm_name = line.split()[1]
            offline_vms.append(vm_name)

    if not offline_vms:
        return 0
    else:
        return offline_vms
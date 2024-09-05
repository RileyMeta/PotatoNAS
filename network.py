import subprocess, socket, psutil, speedtest, threading, time

def sleep(int):
    time.sleep(int)

def get_upload(prev_sent):
    net_io = psutil.net_io_counters()

    bytes_sent = net_io.bytes_sent - prev_sent

    return net_io.bytes_sent, bytes_sent

def get_download(prev_recv):
    net_io = psutil.net_io_counters()

    bytes_recv = net_io.bytes_recv - prev_recv

    return net_io.bytes_recv, bytes_recv

def return_download():
    prev_recv = psutil.net_io_counters().bytes_recv
    # try:
    while True:
        sleep(5)  # Wait for 5 seconds

        prev_recv, net_download = get_download(prev_recv)
        
        return round(net_download / 1000, ndigits=2)

def return_upload():
    prev_sent = psutil.net_io_counters().bytes_sent
    # try:
    while True:
        sleep(5)  # Wait for 5 seconds
        
        prev_sent, net_upload = get_upload(prev_sent)
        
        return round(net_upload / 1000, ndigits=2)

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

def get_download_speed():
    try:
        st = speedtest.Speedtest()
        print("Testing Download speed...")
        download_speed = st.download() / 1000000  # Convert to Mbps
        return round(download_speed, ndigits=2)

    except speedtest.SpeedtestException as e:
        print("An error occurred during the Download test:", str(e))

def get_upload_speed():
    try:
        st = speedtest.Speedtest()
        print("Testing Upload speed...")
        upload_speed = st.upload() / 1000000
        return round(upload_speed, ndigits=2)

    except speedtest.SpeedtestException as e:
        print("An error occurred during the Upload test:", str(e))

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
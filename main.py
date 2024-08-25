from flask import Flask, render_template, redirect
from commands import * # This is where the magic happens


app = Flask(__name__)

#  The Actual App

@app.route("/")
def index():
    active_interface=get_active_network_interface(),
    interface_type=get_network_interface_type(active_interface),
    speedtest=start_speedtest(),
    return render_template('index.html', 
                            cpu=get_cpu_model_name,
                            disk_usage=get_disk_usage,
                            get_logs=get_logs,
                            get_total_memory=get_total_memory, 
                            get_hostname=get_hostname,
                            get_cpu_load=get_cpu_load_average,
                            get_uptime=get_system_uptime,
                            get_ip_address=get_ip_address,
                            VERSION=VERSION,
                            get_kernel_version=get_kernel_version,
                            get_free_memory=get_free_memory,
                            get_used_memory=get_used_memory,
                            get_memory_usage=get_memory_usage,
                            get_cpu_process=get_cpu_process,
                            get_username=get_username,
                            active_interface=active_interface,
                            interface_type=interface_type,
                            get_internet_speed=get_internet_speed,
                            speedtest=speedtest,
                            )


if __name__ == '__main__':
    app.run()

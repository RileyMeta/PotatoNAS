import subprocess, socket, psutil, speedtest, threading, time

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
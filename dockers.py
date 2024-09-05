import subprocess

def get_docker_status():
    result = subprocess.run(["docker", "ps", "-q"], text=True, capture_output=True)
    docker_status = result.stdout.strip()

    if docker_status == "":
        return 0
    else:
        return docker_status

def get_offline_dockers():
    result = subprocess.run(['docker', 'ps', '-f', 'status=exited', '--format', '{{.ID}}'], 
                            text=True, capture_output=True)

    offline_dockers = result.stdout.strip()

    if offline_dockers == "":
        return 0
    else:
        return offline_dockers
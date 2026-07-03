import psutil
import socket

def get_server_health():

    cpu = psutil.cpu_percent(interval=None)

    memory = psutil.virtual_memory().percent

    disk = psutil.disk_usage("C:/").percent

    status = "Healthy"

    if cpu > 80 or memory > 80:
        status = "Warning"

    return [
        {
            "host": socket.gethostname(),
            "cpu": cpu,
            "memory": memory,
            "disk": disk,
            "status": status
        }
    ]
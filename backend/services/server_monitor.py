# services/server_monitor.py

def get_server_health():

    return [
        {
            "host": "server01",
            "cpu": 35,
            "memory": 62,
            "disk": 48,
            "status": "Healthy"
        },
        {
            "host": "server02",
            "cpu": 75,
            "memory": 70,
            "disk": 55,
            "status": "UP"
        }
    ]
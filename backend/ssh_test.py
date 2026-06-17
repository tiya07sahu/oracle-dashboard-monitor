import paramiko

HOST = "YOUR_SERVER_IP"
USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(
        hostname=HOST,
        username=USERNAME,
        password=PASSWORD
    )

    print("✅ SSH Connected Successfully")

    stdin, stdout, stderr = ssh.exec_command("hostname")
    print("Server Name:", stdout.read().decode())

    ssh.close()

except Exception as e:
    print("❌ Error:", e)
import paramiko

HOST = "10.145.1.235"
USERNAME = "trg"
PASSWORD = "trg123"

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(
        hostname=HOST,
        port=22,
        username=USERNAME,
        password=PASSWORD
    )

    print("✅ SSH Connected Successfully")

    stdin, stdout, stderr = ssh.exec_command("hostname")
    print("Server Name:", stdout.read().decode())

    ssh.close()

except Exception as e:
    print("❌ Error:", e)
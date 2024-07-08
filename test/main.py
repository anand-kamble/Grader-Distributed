import paramiko

hosts = [
    "144.174.27.20",
    "144.174.27.17"
]

ssh = paramiko.SSHClient()
ssh.connect(hostname="144.174.27.20")
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("hostname")

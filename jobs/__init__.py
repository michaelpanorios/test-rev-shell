from nautobot.extras.jobs import registered_jobs
from .reverse_shell_job import ReverseShellJob

register_jobs(ReverseShellJob)

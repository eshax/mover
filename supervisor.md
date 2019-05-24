
# scan.conf
[program:scan]
command=python /opt/git/mover/scan.py
autostart=true
stopsignal=QUIT
user=root
startsecs=2
startretries=1
autorestart=true
redirect_stderr=true
stdout_logfile_maxbytes=100MB
stdout_logfile=/opt/log/scan.log
stderr_logfile=/opt/log/scan.err.log

# mover.conf
[program:mover]
command=python /opt/git/mover/mover.py
autostart=true
stopsignal=QUIT
user=root
startsecs=2
startretries=1
autorestart=true
redirect_stderr=true
stdout_logfile_maxbytes=100MB
stdout_logfile=/opt/log/mover.log
stderr_logfile=/opt/log/mover.err.log

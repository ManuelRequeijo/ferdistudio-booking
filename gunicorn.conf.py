import os

# Configuración básica
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Configuración específica para evitar timeouts
graceful_timeout = 30
worker_tmp_dir = "/dev/shm"
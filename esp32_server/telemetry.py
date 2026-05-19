import time
try:
    import ujson as json
except Exception:
    import json

LOG_FILE = 'telemetry.log'

def _timestamp():
    try:
        return time.time()
    except Exception:
        return 0

def log_event(event_type, details=None):
    try:
        entry = {'ts': _timestamp(), 'event': event_type}
        if details is not None:
            entry['details'] = details
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    except Exception as e:
        try:
            print('Telemetry write error:', e)
        except Exception:
            pass

def read_all():
    try:
        with open(LOG_FILE, 'r') as f:
            return f.read()
    except Exception:
        return ''

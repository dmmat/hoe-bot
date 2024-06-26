from deta import Deta  

deta = Deta()

db = deta.Base("data")

def get_shutdown():
    shutdown = db.get("shutdown")
    return shutdown['value']

def get_queue():
    queue = db.get("queue")
    return queue['value']

def get_schedule():
    schedule = db.get("schedule")
    return schedule['value']

def get_status():
    status = db.get("status")
    return status['value']

def update_shutdown(data):
    db.put(str(data), "shutdown")    
    
def update_queue(data):
    db.put(str(data), "queue")
    
def update_schedule(data):
    db.put(str(data), "schedule")

def update_status(data):
    db.put(str(data), "status")
    
def shutdown_changed(new_shutdown):
    shutdown = get_shutdown()
    if shutdown != new_shutdown:
        update_shutdown(new_shutdown)
        return True
    return False

def queue_changed(new_queue):
    queue = get_queue()
    if str(queue) != str(new_queue):
        update_queue(new_queue)
        return True
    return False

def schedule_changed(new_schedule):
    schedule = get_schedule()
    if str(schedule) != str(new_schedule):
        update_schedule(new_schedule)
        return True
    return False

def status_changed(new_status):
    status = get_status()
    if str(status) != str(new_status):
        update_status(new_status)
        return True
    return False
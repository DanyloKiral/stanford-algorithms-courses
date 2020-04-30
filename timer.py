import time

def start_timer(action_name):
    start_time = time.perf_counter()
    print("Starting " + action_name)
    
    def end_timer():
        end_time = time.perf_counter()
        duration_s = end_time - start_time
        print("Finished "  + action_name  + ". Time = " + str(duration_s) + "s")  
        return dict(
            duration_s = duration_s 
        )
    return dict(
        start_time = start_time,
        finish_timer = end_timer
    )
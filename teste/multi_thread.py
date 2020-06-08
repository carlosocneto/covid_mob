import _thread

# Define a function for the thread
def print_time( threadName, delay):
    count = 0
    while True:
        count += 1        

# Create two threads as follows
try:
    _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
    _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
    _thread.start_new_thread( print_time, ("Thread-3", 4, ) )
    _thread.start_new_thread( print_time, ("Thread-4", 4, ) )
    _thread.start_new_thread( print_time, ("Thread-5", 4, ) )
    _thread.start_new_thread( print_time, ("Thread-6", 4, ) )
    _thread.start_new_thread( print_time, ("Thread-7", 4, ) )
    _thread.start_new_thread( print_time, ("Thread-8", 4, ) )
except:
    print ("Error: unable to start thread")

while 1:
    pass
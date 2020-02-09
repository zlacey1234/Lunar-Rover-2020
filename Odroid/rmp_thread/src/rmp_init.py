#!/usr/bin/env python

from system_defines import *
from rmp_interface import RMP
from user_event_handlers import RMPEventHandlers
import sys,time,threading,Queue

"""
Define the update delay or update period in seconds. Must be greater
than the minimum of 0.01s
"""
UPDATE_DELAY_SEC = 0.05

"""
Define whether to log the output data in a file. This will create a unique CSV
file in ./RMP_DATA_LOGS with the filename containing a time/date stamp 
"""
LOG_DATA = True             

"""
The platform address may be different than the one in your config
(rmp_config_params.py). This would be the case if you wanted to update 
ethernet configuration. If the ethernet configuration is updated the
system needs to be power cycled for it to take effect and this should
be changed to match the new values you defined in your config
"""
rmp_addr = ("192.168.1.4",8080) #this is the default value and matches the config 192.168.0.40


"""
Define the main function for the example. It creates a thread to run RMP and handles
passing the events to the user defined handlers in user_event_handlers.py
"""
def rmp_thread():
    """
    Create and response and command queue. The responses will be in the form of 
    a dictionary containing the vaiable name as the key and a converted value
    the names are defined in the feedback_X_bitmap_menu_items dictionaries if a particular
    variable is of interest
    """
    rsp_queue = Queue.Queue()
    cmd_queue = Queue.Queue()
    in_flags  = Queue.Queue()
    out_flags = Queue.Queue()
    
    """
    Create the thread to run RMP
    """
    my_thread = threading.Thread(target=RMP, args=(rmp_addr,rsp_queue,cmd_queue,in_flags,out_flags,UPDATE_DELAY_SEC,LOG_DATA))
    my_thread.daemon = True
    my_thread.start()
    
    """
    Initialize my event handler class
    """
    EventHandler = RMPEventHandlers(cmd_queue,rsp_queue,in_flags)
    
    """
    -------------------------------------------------------------------------------
    User loop starts here modify to make it do what you want. 
    
    You can pipe std_in from another application to the command queue and the response to std out or 
    let the event handlers define everything. That is up to the user. In this example we transition modes, 
    send motion commands (zeroed), play audio songs, and print the response dictionary. The application 
    terminates the thread and exits when all the songs have been played. It is just an example of how to 
    spawn a RMP thread, handle events, and send/receive data
    ------------------------------------------------------------------------------- 
    """

    """
    Generate a goto tractor event
    """
    EventHandler.GotoTractor()

    """
    Run until signaled to stop
    Perform the actions defined based on the flags passed out
    """
    while (True == EventHandler._continue):
        while not out_flags.empty():
           EventHandler.handle_event[out_flags.get()]()
	  
    print("stopped")
   
  
            
"""
This runs everything
"""
rmp_thread()    
    

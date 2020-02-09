#!/usr/bin/env python
"""--------------------------------------------------------------------
COPYRIGHT 2013 SEGWAY Inc.

Software License Agreement:

The software supplied herewith by Segway Inc. (the "Company") for its 
RMP Robotic Platforms is intended and supplied to you, the Company's 
customer, for use solely and exclusively with Segway products. The 
software is owned by the Company and/or its supplier, and is protected 
under applicable copyright laws.  All rights are reserved. Any use in 
violation of the foregoing restrictions may subject the user to criminal 
sanctions under applicable laws, as well as to civil liability for the 
breach of the terms and conditions of this license. The Company may 
immediately terminate this Agreement upon your use of the software with 
any products that are not Segway products.

The software was written using Python programming language.  Your use 
of the software is therefore subject to the terms and conditions of the 
OSI- approved open source license viewable at http://www.python.org/.  
You are solely responsible for ensuring your compliance with the Python 
open source license.

You shall indemnify, defend and hold the Company harmless from any claims, 
demands, liabilities or expenses, including reasonable attorneys fees, incurred 
by the Company as a result of any claim or proceeding against the Company 
arising out of or based upon: 

(i) The combination, operation or use of the software by you with any hardware, 
    products, programs or data not supplied or approved in writing by the Company, 
    if such claim or proceeding would have been avoided but for such combination, 
    operation or use.
 
(ii) The modification of the software by or on behalf of you 

(iii) Your use of the software.

 THIS SOFTWARE IS PROVIDED IN AN "AS IS" CONDITION. NO WARRANTIES,
 WHETHER EXPRESS, IMPLIED OR STATUTORY, INCLUDING, BUT NOT LIMITED
 TO, IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
 PARTICULAR PURPOSE APPLY TO THIS SOFTWARE. THE COMPANY SHALL NOT,
 IN ANY CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL OR
 CONSEQUENTIAL DAMAGES, FOR ANY REASON WHATSOEVER.
 
 \file   user_event_handlers.py

 \brief  This module allows the user to define how to handle events generated
         in rmp_interface.py.

 \Platform: Cross Platform
--------------------------------------------------------------------"""
from system_defines import *
import time,sys,os,rospy, tf
from std_msgs.msg import Float32, Float32MultiArray
from geometry_msgs.msg import Twist
from rmp_thread.msg import OdomSimple

"""
Define some general parameters for the example like various commands 
"""
RMP_CMD = [RMP_MOTION_CMD_ID,0.0,0.0]
RMP_SET_TRACTOR = [RMP_CFG_CMD_ID,RMP_CMD_SET_OPERATIONAL_MODE,TRACTOR_REQUEST]
RMP_SET_STANDBY = [RMP_CFG_CMD_ID,RMP_CMD_SET_OPERATIONAL_MODE,STANDBY_REQUEST]

"""
This is the class that defines how to handle events passed up by the RMP class.
These events currently include:
RMP_IS_DEAD: The main loop should recongize that the RMP thread is no longer alive
             and should try and respawn or kill the main loop
             
RMP_TX_RDY: The RMP class can accept a new command. Commands sent before this event
            will be queued and executed asyncronously. The user should only post new
            commands once this event has been triggered
            
RMP_RSP_DATA_RDY: A response packet is ready for the user.
"""
class RMPEventHandlers:
    def __init__(self,cmd,rsp,inflags):
        """
        Flag to run the loop
        """    
        self._continue = True
        self.start_time = time.time()
        self.old_cmd = None
        self.idx = 0
        self.cmd_queue = cmd
        self.rsp_queue = rsp
        self.inflags = inflags
        self.soc_threshold = 67

        """
        This is the dictionary that the outflags get passed to. Each one can be
        redefined to be passed to whatever user function you would like
        """
        
        self.handle_event = dict({RMP_KILL:sys.exit,
                                  RMP_INIT_FAILED:self.InitFailedExit,
                                  RMP_IS_DEAD:self.Kill_loop,
                                  RMP_TX_RDY:self.Send_Cmd,
                                  RMP_RSP_DATA_RDY:self.Get_Rsp,
                                  RMP_GOTO_STANDBY:self.GotoStandby,
                                  RMP_GOTO_TRACTOR:self.GotoTractor})

        rospy.init_node('velocity_subscriber', anonymous=True)
	
       
    def Send_Cmd(self):
        vel_subscibe = rospy.Subscriber("/cmd_vel", Twist, self.vel_callback)
        if ((time.time() - self.start_time) > .01):
            self.start_time = time.time()
        #print("Navigation Stack command successfully sent to RMP Segway!")
	    
        
        self.cmd_queue.put(RMP_CMD)
        print(RMP_CMD)
    #Sends normalized vel commands to RMP. The navigation stack will send commands ranging from 0-1.4 mps.	
    def vel_callback(self, msg):	
        RMP_CMD[1] = msg.linear.x/0.05
        RMP_CMD[2] = msg.angular.z/.1
        #print ("callback")
                    
    def Get_Rsp(self):
        fb_dict = self.rsp_queue.get()
        
        my_data = [['operational_time   : ',fb_dict["operational_time"]],
                   ['inertial_x_acc_g   : ',fb_dict["inertial_x_acc_g"]],
                   ['inertial_y_acc_g   : ',fb_dict["inertial_y_acc_g"]],
                   ['inertial_x_rate_rps: ',fb_dict["inertial_x_rate_rps"]],
                   ['inertial_y_rate_rps: ',fb_dict["inertial_y_rate_rps"]],
                   ['inertial_z_rate_rps: ',fb_dict["inertial_z_rate_rps"]],
                   ['pse_pitch_deg      : ',fb_dict["pse_pitch_deg"]],
                   ['pse_roll_deg       : ',fb_dict["pse_roll_deg"]],
                   ['pse_roll_rate_dps  : ',fb_dict["pse_roll_rate_dps"]],
                   ['pse_yaw_rate_dps   : ',fb_dict["pse_yaw_rate_dps"]],
                   ['vel_limit_mps      : ',fb_dict["vel_limit_mps"]],
                   ['vel_limit_mps      : ',fb_dict["vel_limit_mps"]],
                   ['linear_accel_mps2  : ',fb_dict["linear_accel_mps2"]],
                   ['linear_vel_mps     : ',fb_dict["linear_vel_mps"]],
                   ['diff_wheel_vel_rps : ',fb_dict["differential_wheel_vel_rps"]],
                   ['battery_0_voltage  : ',fb_dict["front_base_batt_1_soc"]],
                   ['battery_1_voltage  : ',fb_dict["front_base_batt_2_soc"]],
                   ['battery_2_voltage  : ',fb_dict["rear_base_batt_1_soc"]],
                   ['battery_3_voltage  : ',fb_dict["rear_base_batt_2_soc"]]]

        if my_data[15][1]<self.soc_threshold or my_data[16][1]<self.soc_threshold or my_data[17][1]<self.soc_threshold or my_data[18][1]<self.soc_threshold:
            print ("Battery voltage nearing minimum threshold. Please charge before continuing.")
            self._continue = False;


            temp = ""
            for i in range(0,len(my_data)):
                temp += my_data[i][0]+str(my_data[i][1])+"\n"
                
            os.system('clear')
            print (temp)

        #Publish odometry to odom.cpp node which will transform and publish the data using tf
        #Publisher uses custom message OdomSimple (in msg folder)

        odom_pub = rospy.Publisher("/segway/odometry", OdomSimple, queue_size=50)
        odom_simple = OdomSimple()
        odom_simple.odom_info = [my_data[13][1], 0, my_data[14][1]]

        odom_pub.publish(odom_simple)

    def GotoStandby(self):
        self.cmd_queue.put(RMP_SET_STANDBY)
        
    def GotoTractor(self):
        self.cmd_queue.put(RMP_SET_TRACTOR)
        print("In tractor mode")
        
    def InitFailedExit(self):
        print ("RMP initialization failed....") 
        print ("exiting.....")
        self.inflags.put(RMP_KILL)
        self._continue = False
        
    def Kill_loop(self):
        print ("Loop terminated, killing RMP thread and exiting.....")
        self.inflags.put(RMP_KILL)
        self._continue = False

        





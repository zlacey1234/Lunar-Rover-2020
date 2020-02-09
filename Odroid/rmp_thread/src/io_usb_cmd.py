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
demands,liabilities or expenses, including reasonable attorneys fees, incurred 
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
 
 \file   io_eth_cmd.py

 \brief  This module contains the ethernet UDP communication protocol

 \Platform: Cross platform
--------------------------------------------------------------------"""
from utils import convert_byte_data_to_U32, convert_float_to_u32
from crc16 import *
from system_defines import *
from user_event_handlers import RMP_CMD
import socket, serial, time, glob, fnmatch, sys

class IO_USB:
    def __init__(self):
	
        self.success = True;

        """
        Initialize the flag, find all rmp device ports, and initialize the
        baud rate.
        """
        self.init_failed = False;
        self.baud_rate = 115200;
        if (False == self.find_rmp_device_ports()):
            self.init_failed = True;
            self.success = False;
            print("failed")

        """
        Initialize link status counters
        """

        self.dropped_packet = 0;
        self.prev_cmd_time = 0.0;
        self.recieved_items = 0;

    def Send(self,data):
        try:
          self.conn.write(data)      
        except:
          pass
    
    def Receive(self,num_of_return):
        
        """
        The number of bytes expected is the number of 32-bit messages times
        the bytes per 32-bit word
        """    
        num_of_bytes = num_of_return * 4
        
        """
        Try receiving the data up to a maximum size. If it fails
        empty the data
        """
        try:
            data = self.conn.read(1024)
        except:
            data = []
           
            
        """
        If the data is the length expected, convert the byte data to U32 data and return it.
        Otherwise return the None type.
        """
        if (len(data) == num_of_bytes):
            return_data = convert_byte_data_to_U32(data);
        else:
            return_data = None; 
            
        return return_data;

    def Close(self):
        self.conn.close()
	
    def find_rmp_device_ports(self,preferred_list=['*']):
  
        dummy_command = [RMP_CFG_CMD_ID,RMP_CMD_NONE,0]
        #dummy_command = [RMP_CFG_CMD_ID,RMP_CMD_SET_AUDIO_COMMAND,MOTOR_AUDIO_SIMULATE_MOTOR_NOISE]
        #dummy_command = [RMP_MOTION_CMD_ID,1.0,0.0]
        port_discovered = False;
        try:
            self.conn = serial.Serial('/dev/ttyACM4', baudrate=self.baud_rate,timeout = .015,writeTimeout = 0.015);
            print("try")
        except:
            self.conn = serial.Serial('/dev/ttyACM1', baudrate=self.baud_rate,timeout = .015,writeTimeout = 0.015);
        self.conn.flushInput()
        self.Send(self.Convert_RMP_Cmds_for_Serial_Interface(dummy_command))
        if (self.conn.readable() and self.conn.writable()):
            print("USB Port Discovered...")
        print(self.conn.readable())
        print(self.conn.writable())
        data = self.conn.read(1024);

        print("Testing port...")
        if (len(data) != 0):
            print("Data sent successfully.")
            port_discovered = True;
            self.conn.flushInput()
        else:
            print("ERROR: Data transfer failed")
            self.conn.close()
				
                    
	    return port_discovered
	
	
    def Convert_RMP_Cmds_for_Serial_Interface(self,input_cmds):
            """
            Convert a set of commands for the UDP Ethernet interface
            """
            rmp_cmd = [0]*NUM_USB_ETH_BYTES;
            cmds = [0]*3

            cmds[0] = input_cmds[0]
            cmds[1] = int(convert_float_to_u32(input_cmds[1]))
            cmds[2] = int(convert_float_to_u32(input_cmds[2]))

            rmp_cmd[RMP_USB_ETH_CAN_ID_HIGH_INDEX] = int((cmds[0] & 0xFF00) >> 8)
            rmp_cmd[RMP_USB_ETH_CAN_ID_LOW_INDEX]  = int((cmds[0] & 0x00FF))
            rmp_cmd[RMP_USB_ETH_CAN_DATA_0_INDEX]  = int((cmds[1] & 0xFF000000) >> 24)
            rmp_cmd[RMP_USB_ETH_CAN_DATA_1_INDEX]  = int((cmds[1] & 0x00FF0000) >> 16)
            rmp_cmd[RMP_USB_ETH_CAN_DATA_2_INDEX]  = int((cmds[1] & 0x0000FF00) >> 8)
            rmp_cmd[RMP_USB_ETH_CAN_DATA_3_INDEX]  = int((cmds[1] & 0x000000FF))
            rmp_cmd[RMP_USB_ETH_CAN_DATA_4_INDEX]  = int((cmds[2] & 0xFF000000) >> 24)
            rmp_cmd[RMP_USB_ETH_CAN_DATA_5_INDEX]  = int((cmds[2] & 0x00FF0000) >> 16)
            rmp_cmd[RMP_USB_ETH_CAN_DATA_6_INDEX]  = int((cmds[2] & 0x0000FF00) >> 8)
            rmp_cmd[RMP_USB_ETH_CAN_DATA_7_INDEX]  = int((cmds[2] & 0x000000FF))
              

            compute_buffer_crc(rmp_cmd,NUM_USB_ETH_BYTES)


            """
            Convert the string to char data and return it
            """
            rmp_cmd_chars = []
            for x in range(0,len(rmp_cmd)):
                rmp_cmd_chars.append(chr(rmp_cmd[x]))   

            output = ''.join(rmp_cmd_chars)

            return output        
        
        
        

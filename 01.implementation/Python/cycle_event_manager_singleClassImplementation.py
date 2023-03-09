#!/usr/bin/env python

"""
cycle_event_manager.py: CycleEventManagerRevPi class

This class is aimed at controlling the whole Fischertechnik loop process. 
The loop is managed via the RevPi event manager, that is set for being not 
blocking, with a personalised while loop next to the event system. 
"""


import revpimodio2
from time import sleep

class CycleEventManager():
    """Entry point for Fischertechnik Multiprocess Station with Oven control 
    over RevPi."""
    def __init__(self):
        # Instantiate RevPiModIO controlling library
        self.rpi = revpimodio2.RevPiModIO(autorefresh=True)
        # Handle SIGINT / SIGTERM to exit program cleanly
        self.rpi.handlesignalend(self.cleanup_revpi)
        
        # Defining actuators class variables
        # Turn-table - Motor clock wise        
        self.act_turntable_clockwise = False
        # Turn-table - Motor counter-clock wise
        self.act_turntable_counterclockwise = False
        # Conveyor belt - Motor forward
        self.act_conveyor = False
        # Saw - Motor activation
        self.act_saw = False
        # Oven - Carrier oven motor move inside
        self.act_oven_career_inward = False
        # Oven - Carrier oven motor move outside
        self.act_oven_career_outward = False
        # Vacuum carrier - Motor move towards oven
        self.act_vacuum_carrier_to_oven = False
        # Vacuum carrier - Move towards turn-table
        self.act_vacuum_carrier_to_turntable = False
        # Oven - Processing light
        self.act_oven_process_light = False
        # Compressor - activation
        self.act_compressor = False
        # Vacuum carrier - Vacuum valve grip activation
        self.act_carrier_vacuum_gripper = False
        # Vacuum carrier - Vacuum valve lowering activation
        self.act_carrier_vacuum_gripper_lowering = False
        # Oven - Door opening activation
        self.act_vacuum_oven_door = False
        # Turn-table - Pusher valve activation
        self.act_turntable_vacuum_pusher = False

        # Defining sensor class varaibles
        # Reference switch - Turntable under vacuum carrier
        self.sens_turntable_towards_vacuum_ref_switch = False
        # Reference switch - Turntable aligned to position conveyor
        self.sens_turntable_towards_conveyor_ref_switch = False
        # Light sensor - Conveyor belt
        self.sens_conveyor_light_barrier = False
        # Reference switch - Turn-table under saw
        self.sens_turntable_towards_saw_ref_switch = False
        # Reference switch - Vacuum carrier aligned to turn-table
        self.sens_vacuum_gripper_carrier_towards_turntable_ref_switch = False
        # Reference switch - Oven carrier inside the oven
        self.sens_oven_carrier_in_ref_switch = False
        # Reference switch - Oven carrier outside the oven
        self.sens_oven_carrier_out_ref_switch = False
        # Reference switch - Vacuum carrier aligned to oven
        self.sens_vacuum_gripper_carrier_towards_oven_ref_switch = False
        # Light sensor - Oven
        self.sens_oven_light_barrier = False
        
        # Other support time sensors
        self.time_sens_saw_count = 0          # Saw process time counter
        self.time_sens_oven_count = 0         # Oven process time counter
        self.time_sens_vacuum_count = 0       # Vacuum process time counter
        self.time_sens_delivery_count = 0     # Delivery process time counter
        self.counter = 0
        # Other support bool sensors
        self.bool_sens_oven_ready = False     # Oven ready variable

        # Sync sensors digital values with the values of the physical model
        self.read()
        

    def cleanup_revpi(self):
        """Cleanup function to leave the RevPi in a defined state."""
        # Switch of LED and outputs before exit program
        print('Cleaning the system state')
        self.rpi.core.a1green.value = False
        self.rpi.io['O_1'].value = False
        self.rpi.io['O_2'].value = False
        self.rpi.io['O_3'].value = False
        self.rpi.io['O_4'].value = False
        self.rpi.io['O_5'].value = False
        self.rpi.io['O_6'].value = False
        self.rpi.io['O_7'].value = False
        self.rpi.io['O_8'].value = False
        self.rpi.io['O_9'].value = False
        self.rpi.io['O_10'].value = False
        self.rpi.io['O_11'].value = False
        self.rpi.io['O_12'].value = False
        self.rpi.io['O_13'].value = False
        self.rpi.io['O_14'].value = False

    def read(self):
        """Reads the input sensors states"""
        # Assigning to a the relative variable, the sensor value
        # Reference switch - Turntable under vacuum carrier
        self.sens_turntable_towards_vacuum_ref_switch = \
            self.rpi.io['I_1'].value
        # Reference switch - Turntable aligned to position conveyor
        self.sens_turntable_towards_conveyor_ref_switch = \
            self.rpi.io['I_2'].value
        # Light sensor - Conveyor belt
        self.sens_conveyor_light_barrier = \
            self.rpi.io['I_3'].value
        # Reference switch - Turn-table under saw
        self.sens_turntable_towards_saw_ref_switch = \
            self.rpi.io['I_4'].value
        # Reference switch - Vacuum carrier aligned to turn-table
        self.sens_vacuum_gripper_carrier_towards_turntable_ref_switch = \
            self.rpi.io['I_5'].value
        # Reference switch - Oven carrier inside the oven
        self.sens_oven_carrier_in_ref_switch = \
            self.rpi.io['I_6'].value
        # Reference switch - Oven carrier outside the oven
        self.sens_oven_carrier_out_ref_switch = \
            self.rpi.io['I_7'].value
        # Reference switch - Vacuum carrier aligned to oven
        self.sens_vacuum_gripper_carrier_towards_oven_ref_switch = \
            self.rpi.io['I_8'].value
        # Light sensor - Oven
        self.sens_oven_light_barrier = \
            self.rpi.io['I_9'].value
    
    def write(self):
        """Writes the output actuators states"""
        # Assigning to a the relative sensor, the variable value
        # Turn-table - Motor clock wise        
        self.rpi.io['O_1'].value = self.act_turntable_clockwise
        # Turn-table - Motor counter-clock wise
        self.rpi.io['O_2'].value = self.act_turntable_counterclockwise
        # Conveyor belt - Motor forward
        self.rpi.io['O_3'].value = self.act_conveyor
        # Saw - Motor activation
        self.rpi.io['O_4'].value = self.act_saw
        # Oven - Carrier oven motor move inside
        self.rpi.io['O_5'].value = self.act_oven_career_inward
        # Oven - Carrier oven motor move outside
        self.rpi.io['O_6'].value = self.act_oven_career_outward
        # Vacuum carrier - Motor move towards oven
        self.rpi.io['O_7'].value = self.act_vacuum_carrier_to_oven
        # Vacuum carrier - Move towards turn-table
        self.rpi.io['O_8'].value = self.act_vacuum_carrier_to_turntable
        # Oven - Processing light
        self.rpi.io['O_9'].value = self.act_oven_process_light
        # Compressor - activation
        self.rpi.io['O_10'].value = self.act_compressor
        # Vacuum carrier - Vacuum valve grip activation
        self.rpi.io['O_11'].value = self.act_carrier_vacuum_gripper
        # Vacuum carrier - Vacuum valve lowering activation
        self.rpi.io['O_12'].value = self.act_carrier_vacuum_gripper_lowering
        # Oven - Door opening activation
        self.rpi.io['O_13'].value = self.act_vacuum_oven_door
        # Turn-table - Pusher valve activation
        self.rpi.io['O_14'].value = self.act_turntable_vacuum_pusher

    def start(self):
        """Start event system and own cyclic loop."""
        print('start')
        # Start event system loop without blocking here. Reference at 
        # https://revpimodio.org/en/events-in-the-mainloop/
        self.rpi.mainloop(blocking=False)
        # Activating the process services - i.e. the compressor
        self.act_compressor = True
        # My own loop to do some work next to the event system. We will stay
        # here till self.rpi.exitsignal.wait returns True after SIGINT/SIGTERM
        # The loop does 3 things, continuously: 
        #   0. Sets the Rpi a1 light
        #   1. Reads the sensors states
        #   2. Calls the .process_product function
        #   3. Writes the actuators desired states
        while (self.rpi.exitsignal.wait(0.05) == False):
            # Sets the Rpi a1 light: switch on / off green part of LED A1 | or 
            # do other things
            self.rpi.core.a1green.value = not self.rpi.core.a1green.value

            # 1. Reads the sensors states
            self.read()

            # 2. Calls the machine_group.process_product process description
            #self.machine_group.process_product() 
            # If the oven-light sensor is False, that is there is the product
            # TODO: change this entry point to "if the product is on the oven carrier"
            if (self.sens_oven_light_barrier == False):
                # If oven_ready == False
                if (self.bool_sens_oven_ready == False):
                    # Move the carrier towards the oven
                    if (self.sens_vacuum_gripper_carrier_towards_oven_ref_switch == False):
                        # Activate it towards the oven
                        self.act_vacuum_carrier_to_oven = True
                    else:
                        # Deactivate it towards the oven
                        self.act_vacuum_carrier_to_oven = False
                
            # self.oven_process() function
            # If the oven is not ready and the vacuum carrier grip sensor 
            # is True, that is the carrier grip sensor is at the oven: 
            if (self.bool_sens_oven_ready == False and 
                self.sens_vacuum_gripper_carrier_towards_oven_ref_switch == True):
                # If the oven feeder inside sensor is False, that is the 
                # oven carrier  is outside the oven
                if (self.sens_oven_carrier_in_ref_switch == False):
                    # TODO: FROM HERE WRAP INTO A SINGLE FUNCTION
                    # Open the door
                    self.act_vacuum_oven_door = True
                    # Move the feeder in the oven
                    self.act_oven_career_inward = True
                # If the oven feeder is inside the oven
                else:
                    # Deactivate the inward oven
                    self.act_oven_career_inward = False
                    # Close the door
                    self.act_vacuum_oven_door = False
                    # TODO: modify so that the light flashes only AFTER the door is completely closed
                    #haha, flashing lights go brrrr - For light flashing
                    if (self.time_sens_oven_count % 2 == 1):
                        # Activate the process light
                        self.act_oven_process_light = True
                    else:
                        # Deactivate the process light
                        self.act_oven_process_light = False
                    # Time counter
                    self.time_sens_oven_count += 1            

                # If the counter reaches 30, stop the process
                if (self.time_sens_oven_count >= 30):       
                    # Deactivate the light
                    self.act_oven_process_light = False
                    # Set the oven to ready
                    self.bool_sens_oven_ready = True
                    # Set the oven counter to 0
                    self.time_sens_oven_count = 0
            # If the oven is ready
            elif (self.bool_sens_oven_ready == True):
                # TODO: FROM HERE WRAP INTO A SINGLE FUNCTION
                #self.move_feeder_out() function
                # If oven_feeder_out sensor is False = the carrier is not 
                # out
                if (self.sens_oven_carrier_out_ref_switch == False):
                    # Open the door
                    self.act_vacuum_oven_door = True
                    # Move the oven outside
                    self.act_oven_career_outward = True
                else:
                    # Stop moving the oven carrier
                    self.act_oven_career_outward = False
                    # Close the door
                    self.act_vacuum_oven_door = False
                        
                # Take the product with the carrier grip
                # Lower the vacuum gripper
                # If oven feeder sensor is True and oven ready is True and the
                # vacuum gripper variable is True and vacuum counter is less
                # than 10, that is if the oven feeder is out from the oven and
                # the oven is in ready state and the vacuum carrieer gripper 
                # is at the oven and the vacuum counter is less than 10
                # The counter is needed in order to wait for the vacuum gripper
                # to be completely lowered  
                if (self.sens_oven_carrier_out_ref_switch == True 
                    and self.bool_sens_oven_ready == True
                    and self.sens_vacuum_gripper_carrier_towards_oven_ref_switch == True 
                    and self.time_sens_vacuum_count < 10):
                    # Lower the carrier vacuum gripper
                    self.act_carrier_vacuum_gripper_lowering = True
                    # Add 1 to the vacuum counter
                    self.time_sens_vacuum_count += 1
                
                # Grip the product 
                # If vacuum count is greater than 10 and less than 15
                if (self.time_sens_vacuum_count >= 10 and 
                    self.time_sens_vacuum_count < 15):
                    # Activate the carrier vacuum gripper
                    self.act_carrier_vacuum_gripper = True 
                    # Add 1 to the vacuum count
                    self.time_sens_vacuum_count += 1

                # Raise the vacuum gripper 
                # If vacuum count is greater than 15 and less than 25
                if (self.time_sens_vacuum_count >= 15 and 
                      self.time_sens_vacuum_count < 25):
                    # Upper the carrier vacuum gripper
                    self.act_carrier_vacuum_gripper_lowering = False
                    # Add 1 to the vacuum counter
                    self.time_sens_vacuum_count += 1

                # Wait 5 cycles
                # If vacuum count is greater than 25 and less than 30
                #if (self.time_sens_vacuum_count >= 25 and 
                #      self.time_sens_vacuum_count < 30):
                        # Add 1 to the vacuum count
                        #self.time_sens_vacuum_count += 1
                
                # Move the carrier to the turntable
                # If vacuum count is greater than 30
                if (self.time_sens_vacuum_count >= 25):
                    # Bring the carrier vacuum gripper to the turn-table
                    if (self.sens_vacuum_gripper_carrier_towards_turntable_ref_switch == False):
                        self.act_vacuum_carrier_to_turntable = True
                    else:
                        self.act_vacuum_carrier_to_turntable = False
                
                # Release the product
                # Lower the carrier vacuum gripper
                if (self.sens_vacuum_gripper_carrier_towards_turntable_ref_switch == True 
                    and self.act_carrier_vacuum_gripper == True
                    and self.counter < 15):
                        self.act_carrier_vacuum_gripper_lowering = True
                        self.counter += 1
                        print('counter ' + str(self.counter))
                # Release the product on the turntable
                elif (self.sens_vacuum_gripper_carrier_towards_turntable_ref_switch == True 
                    and self.act_carrier_vacuum_gripper_lowering == True
                    and self.counter >= 15 and self.counter < 30):
                        self.act_carrier_vacuum_gripper = False
                        self.counter += 1
                        print('counter ' + str(self.counter))
                # Raise the carrier vacuum gripper
                elif (self.sens_vacuum_gripper_carrier_towards_turntable_ref_switch == True 
                    and self.act_carrier_vacuum_gripper_lowering == True
                    and self.act_carrier_vacuum_gripper == False
                    and self.counter >= 30):
                        self.act_carrier_vacuum_gripper_lowering = False

                # Turn the turntable towards the saw

                # Activate the saw

                # Turn the turntable towards the conveyor

                # Activate the conveyor
                
                """
                # Deliver the product (where?)
                #self.deliver_product() function
                # If the conveyor light sensor is True and the vacuum count is 
                # greter than 30 and the carrier vacuum gripper at turntable is 
                # True, that is if the processing sensor delivery have no 
                # product and the vacuum counter is greater that 30 and the 
                # vacuum gripper carrier is at the turntable
                if (self.sens_conveyor_light_barrier == True 
                    and self.time_sens_vacuum_count >= 25 
                    and self.sens_vacuum_gripper_carrier_towards_turntable_ref_switch == True):
                    # if the delivery count is smaller than 15
                    if (self.time_sens_delivery_count < 15):
                        # Activate the compressor
                        #self.act_compressor = True
                        # Lower the carrier vacuum grip
                        #self.act_carrier_vacuum_gripper_lowering = True
                        # Add 1 to the delivery count
                        self.time_sens_delivery_count += 1
                    # if the delivery count is greater than 15 and smaller than 
                    # 25
                    elif (self.time_sens_delivery_count < 25 and 
                          self.time_sens_delivery_count >= 15):
                        # Deactivate the gripper valve
                        self.act_carrier_vacuum_gripper = False
                        # Add 1 to the delivery count
                        self.time_sens_delivery_count += 1
                    # if the delivery count is greater than 25 and smaller than 
                    # 35
                    elif (self.time_sens_delivery_count < 35 and 
                          self.time_sens_delivery_count >= 25):
                        # Upper the carrier vacuum valve
                        self.act_carrier_vacuum_gripper_lowering = False
                        # Add 1 to the delivery count
                        self.time_sens_delivery_count += 1
                    else:
                        # If the saw count is 0
                        if (self.time_sens_saw_count == 0):
                            # Rotate the turn-table towards the saw
                            #self.turntable_to_saw() function
                            # If the turntable_pos_say sensor is False and the 
                            # turntable_pos_conveyor is False that is
                            # if the turn-table is not aligned under the saw 
                            # and is not at the conveyor
                            if (self.sens_turntable_towards_saw_ref_switch == False 
                                and self.sens_turntable_towards_conveyor_ref_switch == False):
                                # Activate the turn-table rotation clockwise
                                self.act_turntable_clockwise = True 
                            else:
                                # Deactivate the turn-table rotation clockwise
                                self.act_turntable_clockwise = False    
                            
                        # Activate the saw
                        #self.use_saw() function
                        # If the turntable_pos_saw sensor is True and saw 
                        # counter is not greater than 20 that is if 
                        # turntable_pos_saw is under the saw and saw counter is 
                        # not greater than 20
                        if (self.sens_turntable_towards_saw_ref_switch == True 
                            and self.time_sens_saw_count < 20):
                            # Activate the saw
                            self.act_saw  = True
                            # Add 1 to the saw counter
                            self.time_sens_saw_count += 1
                        else:
                            # Deactivate the saw
                            self.act_saw  = False 

                        # If the saw conter is greater than 20
                        if (self.time_sens_saw_count >= 20):
                            # Rotate the turn-table toward the conveyor
                            #self.turntable_to_conveyor() function
                            # If the turntable_pos_conveyor sensor is False
                            if (self.sens_turntable_towards_conveyor_ref_switch == False):
                                # Activate the turntable rotation clockwise
                                self.act_turntable_clockwise = True
                            else:
                                # Deactivate the turntable rotation clockwise
                                self.act_turntable_clockwise = False

                        # If the turntable_pos_conveyor is True
                        if (self.sens_turntable_towards_conveyor_ref_switch == True):
                            # Activate the conveyor
                            #self.act_compressor = True
                            # Activate the turntable pusher
                            self.act_turntable_vacuum_pusher = True
                            # Activate the conveyor
                            self.act_conveyor = True
                    """
            # Otherwise, if there is the product in front of the light sensor
            if(self.sens_conveyor_light_barrier == False):    
                # Turn off the services
                self.act_compressor = False
                
                # Turn off the valve feeder
                self.act_turntable_vacuum_pusher = False
                
                # Turn off the conveyor belt
                self.act_conveyor = False
                
                # Turn the turn-table towards the carrier
                #self.turntable_to_vacuum() function
                # If the turntable_pos_vacuum sensor is False, that is 
                # if the turntable is not at the vacuum gripper carrier
                if (self.sens_turntable_towards_vacuum_ref_switch == False):
                    # Activate the conveyor rotation clockwise
                    self.act_turntable_counterclockwise = True
                # Otherwise, if the turntable_pos_vacuum sensor is True, that 
                # is if the turntable is at the vacuum gripper carrier
                else:
                    # Deactivate the conveyor rotation clockwise
                    self.act_turntable_counterclockwise = False

                # If the turntable faces the carrier
                if (self.sens_turntable_towards_vacuum_ref_switch == True):
                    # Reset all stations
                    #self.reset_station() function    
                    #print('resetStation')
                    # Resets all counters
                    self.time_sens_saw_count = 0
                    self.time_sens_oven_count = 0
                    self.time_sens_vacuum_count = 0
                    self.time_sens_delivery_count = 0
                    # Sets the oven as "not ready"
                    self.bool_sens_oven_ready = False 

            # 3. Writes the actuators desired states
            self.write()


if __name__ == "__main__":
    # Instantiating the controlling class
    root = CycleEventManager()
    # Launch the start function of the RevPi event control system
    root.start()

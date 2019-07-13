"""
Demo the trick flying for the python interface

Author: Amy McGovern
"""



from pyparrot.Minidrone import Mambo
from mymodule.MyDroneVisionGUI import DroneVisionGUI

import time

# If you are using BLE: you will need to change this to the address of YOUR mambo
# if you are using Wifi, this can be ignored
mamboAddr = "e0:14:d0:63:3d:d0"

# make my mambo object
# remember to set True/False for the wifi depending on if you are using the wifi or the BLE to connect
mambo = Mambo(mamboAddr, use_wifi=True)

print("trying to connect")
success = mambo.connect(num_retries=3)
print("connected: %s" % success)

# success = True
started = False


def start():
    print("sleeping")
    mambo.smart_sleep(2)
    mambo.ask_for_state_update()
    mambo.smart_sleep(2)

    started = True

    print("taking off!")
    mambo.safe_takeoff(1)


def land():
    print("landing")
    print("flying state is %s" % mambo.sensors.flying_state)
    mambo.safe_land(5)
    mambo.smart_sleep(1)


def move(roll, pitch, yaw, vertical, duration, sleep):
    if (mambo.sensors.flying_state != "emergency"):
        print("flying state is %s" % mambo.sensors.flying_state)
        print(F"roll:{roll}, pitch:{pitch}, yaw:{yaw}, vertical:{vertical}, duration:{duration}, sleep:{sleep}")
        mambo.fly_direct(roll=roll, pitch=pitch, yaw=yaw, vertical_movement=vertical, duration=duration)
        mambo.smart_sleep(sleep)

    else:
        land()

def controll(mamboVision, args):
    if (success):
        # get the state information

        start()

        roll = 0
        pitch = 0
        yaw = 0
        vert = 0
        dur = 1
        sleep = 1

        menu = F"""
            1) roll 
            2) pitch 
            3) yaw 
            4) vertical 
            5) duration 
            6) sleep 
            q) quit
        """
        inp = ""

        while not (inp == "q"):
            print(menu)
            inp = input("Choice: ")

            if (inp == "1"):
                roll = int(input("\t roll: "))
                move(roll, pitch, yaw, vert, dur, sleep)
                roll = 0

            elif (inp == "2"):
                pitch = int(input("\t pitch: "))
                move(roll, pitch, yaw, vert, dur, sleep)
                pitch = 0

            elif (inp == "3"):
                yaw = int(input("\t yaw: "))
                move(roll, pitch, yaw, vert, dur, sleep)
                yaw = 0

            elif (inp == "4"):
                vert = int(input("\t vert: "))
                move(roll, pitch, yaw, vert, dur, sleep)
                vert = 0

            elif (inp == "5"):
                dur = int(input("\t duration: "))

            elif (inp == "6"):
                sleep = int(input("\t sleep: "))

            elif (inp == "q"):

                land()
                print("disconnect")
                mambo.disconnect()
                exit(0)

            else:
                pass

            print(mambo.sensors)

# start()
# controll(None, None)

print("Preparing to open vision")
mamboVision = DroneVisionGUI(mambo, is_bebop=False, buffer_size=50,
                             user_code_to_run=controll, user_args=(mambo, ))
# mamboVision.set_user_callback_function(userVision.save_pictures, user_callback_args=None)
mamboVision.open_video()



## roll - positve right, negative left
## pitch - positive forward, negative backward
## yaw - positive - clockwise, negative - anticlockwis

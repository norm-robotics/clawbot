# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
ArmMotor_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_36_1, True)
ArmMotor_motor_b = Motor(Ports.PORT11, GearSetting.RATIO_36_1, False)
ArmMotor = MotorGroup(ArmMotor_motor_a, ArmMotor_motor_b)
ClawMotor = Motor(Ports.PORT2, GearSetting.RATIO_36_1, False)

ClawMotor.set_stopping(HOLD)
ArmMotor.set_stopping(HOLD)
left_front_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
right_front_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
right_back_motor = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
left_back_motor = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
left_motor = MotorGroup(left_back_motor, left_front_motor)
right_motor = MotorGroup(right_back_motor, right_front_motor)

def control_arm():
    if(controller_1.buttonUp.pressing()): 
        ArmMotor.spin(REVERSE)
    elif(controller_1.buttonDown.pressing()):
        ArmMotor.spin(FORWARD)
    else:
        ArmMotor.stop()

def control_claw():
    if(controller_1.buttonRight.pressing()):
        ClawMotor.spin(FORWARD)
    elif(controller_1.buttonLeft.pressing()):
        ClawMotor.spin(REVERSE)
    else:
        ClawMotor.stop()

def control_drive():
    drive_velocity = controller_1.axis3.position()
    turn_velocity = controller_1.axis4.position()

    right_motor_speed = 0
    left_motor_speed = 0
    if abs(drive_velocity) > 10:
        right_motor_speed += drive_velocity
        left_motor_speed += drive_velocity
    right_motor_speed += turn_velocity
    left_motor_speed -= turn_velocity


    left_motor.spin(FORWARD,left_motor_speed,PERCENT)
    right_motor.spin(FORWARD,right_motor_speed,PERCENT)
    
# Main loop
while True:
    if((left_motor.temperature(TemperatureUnits.CELSIUS) > 40) or (right_motor.temperature(TemperatureUnits.CELSIUS) > 40) or (right_front_motor.temperature(PERCENT) > 40) or (ArmMotor.temperature(TemperatureUnits.CELSIUS) > 40) or (ClawMotor.temperature(PERCENT) > 60)):
        controller_1.screen.set_cursor(1,1)
        controller_1.screen.print("Motors Overheating!")
        controller_1.screen.next_row()
        controller_1.screen.print("Please unplug and remove battery from brain!")
        controller_1.rumble("-..-..")
        wait(30, SECONDS)
        brain.program_stop()
    else:
        control_drive()
        control_arm()
        control_claw()
        wait(20, MSEC)
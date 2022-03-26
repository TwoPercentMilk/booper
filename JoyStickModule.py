import pygame
from time import sleep

pygame.init()
# ID #0
controller = pygame.joystick.Joystick(0)
# Initialize controller
controller.init()

# Create dictionary of buttons
# 0 = not pressed, 1 = pressed
# Axes describe up/down/left/right of each of the 2 joysticks
buttons = {'x': 0, 'o': 0, 't': 0, 's': 0,
           'L1': 0, 'R1': 0, 'L2': 0, 'R2': 0,
           'share': 0, 'options': 0,
           'axis1': 0, 'axis2': 0, 'axis3': 0, 'axis4': 0}
axis_list = [0., 0., 0., 0., 0., 0.]


def get_joystick(name=''):
    global buttons
    # Retrieve events in pygame
    for event in pygame.event.get():
        # Check if analogue stick moves
        if event.type == pygame.JOYAXISMOTION:  # Analogue stick movement
            axis_list[event.axis] = round(event.value, 2)
        elif event.type == pygame.JOYBUTTONDOWN:  # Button press
            # If button is pressed, replace 0 in dict with 1
            for x, (key, val) in enumerate(buttons.items()):
                if x < 10:
                    if controller.get_button(x):
                        buttons[key] = 1
        elif event.type == pygame.JOYBUTTONUP:  # Button release
            for x, (key, val) in enumerate(buttons.items()):
                if x < 10:
                    if event.button == x:
                        buttons[key] = 0

    # Correctly number axes as 0, 1, 3, 4
    # LEFT JOYSTICK:  axis1 -> (left, right) // axis2 -> (up, down)
    # RIGHT JOYSTICK: axis3 -> (left, right) // axis4 --> (up, down)
    buttons['axis1'], buttons['axis2'], buttons['axis3'], buttons['axis4'] =\
        [axis_list[0], axis_list[1], axis_list[3], axis_list[4]]

    # Return all values of buttons dict if no name is specified
    if name == '':
        return buttons
    else:
        return buttons[name]


def main():
    print(get_joystick())
    sleep(.05)

    # To get output of one button/axis
    # print(get_joystick('x'))
    # sleep(.05)


if __name__ == '__main__':
    while True:
        main()

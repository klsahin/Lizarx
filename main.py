import pygame
from classes import *
import random
arduino = False
'''
# ARDUINO SETUP
import serial
import serial.tools.list_ports
import time
import csv



if arduino:
    # Identify the correct port
    ports = serial.tools.list_ports.comports()
    for port in ports: print(port.device, port.name)

    # Create CSV file
    f = open("data.csv","w",newline='')
    f.truncate()

    # Open the serial com
    serialCom = serial.Serial('/dev/cu.usbserial-110',115200)

    # Toggle DTR to reset the Arduino
    serialCom.setDTR(False)
    time.sleep(1)
    serialCom.flushInput()
    serialCom.setDTR(True)

    # How many data points to record (if stopping)
    kmax = 150

    # Loop through and collect data as it is available
    dataVariable = 0


'''

screenWidth = 700
screenHeight = 800

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
running = True


# Load Object
leaves = Leaves(screenWidth, screenHeight)
tree = Tree(screenWidth,screenHeight)
tree.load_image()
lizard = Lizard(300, 500, 200, 300, 1)  # Example parameters for lizard
lizard.load_image()

# draw all objects
def draw_objects():
    #draw background
    leaves.draw(screen)
    tree.draw(screen)
    #draw lizard
    screen.blit(lizard.image, lizard.position)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        lizard.turn(False, False, False, False, screen, leaves, tree)
    elif keys[pygame.K_u]:
        lizard.turn(False, True, False, False, screen, leaves, tree)
    elif keys[pygame.K_h]:
        lizard.turn(True, True, False, False, screen, leaves, tree)
    elif keys[pygame.K_i]:
        lizard.turn(False, False, True, False, screen, leaves, tree)
    elif keys[pygame.K_l]:
        lizard.turn(False, False, True, True, screen, leaves, tree)


    draw_objects()  # Call the function to draw objects
    pygame.display.flip()  # Update the display

""" 
    try:
        
        if arduino:
            pass
            # serialCom.flushInput()  # Clear the input buffer
            # s_bytes = serialCom.readline()
            # decoded_bytes = s_bytes.decode("utf-8").strip('\r\n')
            # print(f"decoded bytes: {decoded_bytes}")
            # farLeftData = []
            # topLeftData = []
            # topRightData = []
            # farRightData = []
            # count = 0

            # # Split the data by commas and store in leftData and rightData
            # for data in decoded_bytes.split(","):
            #     if count < 2:
            #         farLeftData.append(data)
            #     elif count < 4:
            #         topLeftData.append(data)
            #     elif count < 6:
            #         topRightData.append(data)
            #     elif count < 8:
            #         farRightData.append(data)

            #     count += 1
        else: # Simulate data with. H, U, I, L keys
            complete = False
            for key in pygame.key.get_pressed():
                if key == pygame.K_h:
                    farLeftData = [2000,2000]
                elif key == pygame.K_u:
                    topLeftData = [2000,2000]
                elif key == pygame.K_i:
                    topRightData = [2000,2000]
                elif key == pygame.K_l:
                    farRightData = [2000,2000]
                complete = True
            if not complete:
                farLeftData = [0, 0]
                topLeftData = [0, 0]
                topRightData = [0, 0]
                farRightData = [0, 0]
        
        farLeftTurn = False
        topLeftTurn = False
        topRightTurn = False
        farRightTurn = False

        # Turning Logic
        for data in farLeftData:
            if int(data) > 1500:
                farLeftTurn = True
        for data in topLeftData:
            if int(data)  > 1500:
                topLeftTurn = True
        for data in topRightData:
            if int(data)  > 1500:
                topRightTurn = True
        for data in farRightData:
            if int(data)  > 1500:
                farRightTurn = True
        
        lizard.turn(farLeftTurn, topLeftTurn, topRightTurn, farRightTurn, screen, background)
        pygame.time.delay(100)  # Delay to control the speed of the loop    

    except:
        print("Error reading data from serial port")
        farLeftTurn = topLeftTurn = topRightTurn = farRightTurn = False
        
     """
    

pygame.quit()
f.close()  # Close the CSV file
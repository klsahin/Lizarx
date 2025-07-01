import pygame
from classes import *
import random


# ARDUINO SETUP
import serial
import serial.tools.list_ports
import time
import csv

arduino = False

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





pygame.init()
screen = pygame.display.set_mode((800, 600))
running = True


# Load Object
background = Background(800, 600)
lizard = Lizard(400, 400, 50, 50, 0)  # Example parameters for lizard

# draw all objects
def draw_objects():
    #draw background
    background.draw(screen)
    #draw lizard
    screen.blit(lizard.image, lizard.position)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    try:
        if arduino:
            serialCom.flushInput()  # Clear the input buffer
            s_bytes = serialCom.readline()
            decoded_bytes = s_bytes.decode("utf-8").strip('\r\n')
            print(f"decoded bytes: {decoded_bytes}")
            farLeftData = []
            topLeftData = []
            topRightData = []
            farRightData = []
            count = 0

            # Split the data by commas and store in leftData and rightData
            for data in decoded_bytes.split(","):
                if count < 2:
                    farLeftData.append(data)
                elif count < 4:
                    topLeftData.append(data)
                elif count < 6:
                    topRightData.append(data)
                elif count < 8:
                    farRightData.append(data)

                count += 1
        else: # Simulate data with. H, U, I, L keys
            for key in pygame.key.get_pressed():
                if key == pygame.K_h:
                    farLeftData = [2000,2000]
                elif key == pygame.K_u:
                    topLeftData = [2000,2000]
                elif key == pygame.K_i:
                    topRightData = [2000,2000]
                elif key == pygame.K_l:
                    farRightData = [2000,2000]
                else:
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
        

    draw_objects()  # Call the function to draw objects
    pygame.display.flip()  # Update the display



pygame.quit()
f.close()  # Close the CSV file
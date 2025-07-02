import pygame
from classes import *
import random
arduino = True

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




screenWidth = 700
screenHeight = 800

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
running = True


# Load Object
leaves = Leaves(screenWidth, screenHeight)
tree = Tree(screenWidth,screenHeight)
tree.load_image()
lizard = Lizard(300, 400, 260, 390, 1)  # Example parameters for lizard
lizard.load_image()

# draw all objects
def draw_objects():
    #draw background
    leaves.draw(screen)
    tree.draw(screen)
    # lizard drawing is now handled in lizard.update()

prev_input = (False, False, False, False)

def checkKeys(prev_input):
    keys = pygame.key.get_pressed()
    input_tuple = (
        keys[pygame.K_a] or keys[pygame.K_h],  # farLeft
        keys[pygame.K_w] or keys[pygame.K_u],  # topLeft
        keys[pygame.K_s] or keys[pygame.K_i],  # topRight
        keys[pygame.K_d] or keys[pygame.K_l],  # farRight
    )
    
start = True
score = 0
objectsOnScreen = []

font_path = 'assets/SuperBubble.ttf'
font = pygame.font.Font(font_path, 64)  # Adjust size as needed
font_color = (255, 140, 0)


def collisionDetection(objectsOnScreen):
    if objectsOnScreen == []: return None
    x_overlap = False
    y_overlap = False
    for object in (objectsOnScreen):
        x_overlap = (lizard.x < object.x + object.width and lizard.x + lizard.width > object.x)
        y_overlap = (lizard.y < object.y + object.height and lizard.y + lizard.height > object.y)
        if x_overlap and y_overlap:
            return str(object)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #prev_input = checkKeys(prev_input)

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


        farLeftTurn = False
        topLeftTurn = False
        topRightTurn = False
        farRightTurn = False
        

        # Turning Logic
        threshold = 2000
        if int(farLeftData[0]) > threshold and int(farLeftData[1]) > threshold:
            farLeftTurn = True
        if int(topLeftData[0]) > 3000 and int(topLeftData[1]) > threshold:
            topLeftTurn = True
        if int(topRightData[0]) > threshold and int(topRightData[1]) > threshold:
            topRightTurn = True
        if int(farRightData[0]) > threshold and int(farRightData[1]) > threshold:
            farRightTurn = True
        
        
        input_tuple = (farLeftTurn, topLeftTurn, topRightTurn, farRightTurn)
        if input_tuple != (False, False, False, False):
            start = False

        if input_tuple != prev_input or start == True:
            lizard.set_direction(*input_tuple)
            prev_input = input_tuple
    

        leaves.draw(screen)
        tree.scroll(11)
        tree.draw(screen)
        score_text = font.render(str(score), True, font_color)
        screen.blit(score_text, (40,30))
        lizard.update(screen, leaves, tree)
        pygame.display.flip()

        if collisionDetection(objectsOnScreen) == "fruit":
            score += 5
            # something good happens
        elif collisionDetection(objectsOnScreen) == "obstacle":
            score -= 5
            # something bad happens



        #lizard.turn(farLeftTurn, topLeftTurn, topRightTurn, farRightTurn, screen, background)
        #pygame.time.delay(100)  # Delay to control the speed of the loop

    except:
        print("Error reading data from serial port")
        farLeftTurn = topLeftTurn = topRightTurn = farRightTurn = False

     


pygame.quit()
f.close()  # Close the CSV file

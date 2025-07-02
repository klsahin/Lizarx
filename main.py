import pygame
from classes import *
import random

arduino = False  # Set to True to use Arduino, False to use keyboard

if arduino:
    import serial
    import serial.tools.list_ports
    import time
    import csv

    # Identify the correct port
    ports = serial.tools.list_ports.comports()
    for port in ports: print(port.device, port.name)

    # Create CSV file
    f = open("data.csv","w",newline='')
    f.truncate()

    # Open the serial com
    serialCom = serial.Serial('/dev/cu.usbserial-110',115200)

    # Toggle DTR to reset the Arduino
    serialCom.dtr = False
    time.sleep(1)
    serialCom.reset_input_buffer()
    serialCom.dtr = True

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

# Lane positions for fruit (divide crawlable path into 3 lanes)
lane_x = [160 + 15, 300 + 15, 440 + 15]  # Shift all lanes 15 pixels to the right
fruit_width = 75
fruit_height = 75
fruit_spawn_y = -80  # Start just above the screen
fruits = []
max_fruits = 3

# Only one fruit at a time, randomly in one of the three lanes
active_fruit = None

def spawn_single_fruit():
    lane = random.choice([0, 1, 2])
    fruit_type = random.randint(1, 3)
    return Fruit(lane_x[lane], fruit_spawn_y, fruit_width, fruit_height, fruit_type)

active_fruit = spawn_single_fruit()

def draw_objects():
    leaves.draw(screen)
    tree.draw(screen)
    # lizard drawing is now handled in lizard.update()

prev_input = (False, False, False, False)
start = True
score = 0
objectsOnScreen = []

font_path = 'assets/SuperBubble.ttf'
font = pygame.font.Font(font_path, 64)  # Adjust size as needed
font_color = (187, 220, 5)  # #bbdc05 green


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

    try:
        if arduino:
            serialCom.reset_input_buffer()  # Clear the input buffer
            s_bytes = serialCom.readline()
            decoded_bytes = s_bytes.decode("utf-8").strip('\r\n')
            print(f"decoded bytes: {decoded_bytes}")
            farLeftData = []
            topLeftData = []
            topRightData = []
            farRightData = []
            count = 0
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
        else:
            keys = pygame.key.get_pressed()
            input_tuple = (
                keys[pygame.K_a] or keys[pygame.K_h],  # farLeft
                keys[pygame.K_w] or keys[pygame.K_u],  # topLeft
                keys[pygame.K_s] or keys[pygame.K_i],  # topRight
                keys[pygame.K_d] or keys[pygame.K_l],  # farRight
            )
        if input_tuple != (False, False, False, False):
            start = False
        if input_tuple != prev_input or start == True:
            lizard.set_direction(*input_tuple)
            prev_input = input_tuple
        leaves.draw(screen)
        tree.scroll(11)
        tree.draw(screen)
        score_text = font.render(str(score), True, font_color)
        screen.blit(score_text, (20, 20))
        lizard.update(screen, leaves, tree)

        # Move and draw the single fruit
        objectsOnScreen = []
        if active_fruit:
            active_fruit.y += 11  # Move down with the tree scroll speed
            active_fruit.position[1] = active_fruit.y
            active_fruit.load_image(screen)
            objectsOnScreen.append(active_fruit)
            if active_fruit.y > screenHeight:
                active_fruit = spawn_single_fruit()

        pygame.display.flip()

        # Collision detection
        collided = collisionDetection(objectsOnScreen)
        if collided is not None:
            # Check if the collided object is a fruit
            if isinstance(active_fruit, Fruit) and collided == str(active_fruit):
                score += 5
                active_fruit = spawn_single_fruit()
            # If you add obstacles, handle them here

        #lizard.turn(farLeftTurn, topLeftTurn, topRightTurn, farRightTurn, screen, background)
        #pygame.time.delay(100)  # Delay to control the speed of the loop

    except:
        print("Error reading data from serial port")
        farLeftTurn = topLeftTurn = topRightTurn = farRightTurn = False

if arduino:
    f.close()  # Close the CSV file
pygame.quit()

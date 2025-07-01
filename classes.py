import pygame

class Background:
    def __init__(self, width, height, path1 = "assets/background1", path2 = "assets/background2"):
        self.position = [0, 0]
        self.size = [width, height]
        self.imagePath1 = path1
        self.imagePath2 = path2
        self.image1 = None
        self.image2 = None
        self.y_offset = 0

    def load_image(self):
        self.image1 = pygame.image.load(self.imagePath1).convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, self.size)
        self.image2 = pygame.image.load(self.imagePath2).convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, self.size)

    def draw(self, screen):
        # Draw two backgrounds side by side for endless effect
        w = self.size[1]
        y = -self.y_offset % w
        screen.blit(self.image1, (0, y))
        screen.blit(self.image2, (0, y - w))
        # If x > 0, draw the second background before the first
        if y > 0:
            screen.blit(self.image2, (0, y + w))

    def scroll(self, dy):
        self.y_offset += dy

class Lizard:
    def __init__(self, x, y, width, height, index): 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.position = [self.x, self.y]
        self.size = [width, height]
        self.index = index
        self.path = f'assets/lizard{self.index+1}.png' #based on numbering system
        self.image = None  # Placeholder for the image, to be loaded later

    def load_image(self):
        self.image = pygame.image.load(self.path).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
    
    def run(self):
        #straight movement
        pass
    
    def turn(self, farLeft, topLeft, topRight, farRight, screen, background):
        if farLeft and topLeft:
            print("Turning far left")
            #animation
            turn_frames = []
            #position change
            dx = - 10
            dy = 0
            

        elif farLeft or topLeft: # xor: small turn
            print("Turning top left")
            #animation
            turn_frames = []
            #position change
            dx = - 5
            dy = 5
            
        elif topRight and farRight:
            print("Turning far right")
            #animation
            turn_frames = []
            #position change
            dx = 10
            dy = 0

        elif topRight or farRight: # xor: small turn
            print("Turning top right")
            #animation
            turn_frames = []
            #position change
            dx = 5
            dy = 5

        for frame in turn_frames:
            #redraw background
            background.scroll(dy)
            background.draw(screen)

            #update lizard position and image
            self.path = f'assets/lizard{frame}.png'
            self.position[0] += dx
            self.position[1] += dy

            self.load_image()
            screen.blit(self.image, self.position)
            pygame.display.flip()
            pygame.time.delay(100)  # Delay to control the speed of the turn
            



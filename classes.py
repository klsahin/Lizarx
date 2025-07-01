import pygame


class Leaves:
    def __init__(self, width, height, path = "assets/leaves.png"):
        self.position = [0,0]
        self.size = [width, height]
        self.imagePath = path
    
    def draw(self, screen):
        self.image = pygame.image.load(self.imagePath).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        screen.blit(self.image, self.position)

class Tree:
    def __init__(self, width, height, path1 = "assets/tree.png", path2 = "assets/tree2.png"):
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
        y = self.y_offset % w
        screen.blit(self.image1, (0, y - w))
        screen.blit(self.image2, (0, y))
        
        """ w = self.size[1]
        y = self.y_offset % w #scrolls downwards
        screen.blit(self.image1, (0, y))
        screen.blit(self.image2, (0, y + w))
        # If x > 0, draw the second background before the first
        if y > 0:
            screen.blit(self.image2, (0, y - w)) """

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
        self.flip = False # left
        self.path = f'assets/straight/S1.png' #based on numbering system
        self.image = None  # Placeholder for the image, to be loaded later

    def load_image(self):
        self.image = pygame.image.load(self.path).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.image = pygame.transform.flip(self.image, self.flip, False)
    
    
        
    
    def turn(self, farLeft, topLeft, topRight, farRight, screen, leaves, tree):
        if farLeft and topLeft:
            print("Turning far left")
            #animation
            direction = "farLeft/FL"
            #position change
            dx = - 10
            dy = 5
            self.flip = False
            

        elif farLeft or topLeft: # xor: small turn
            print("Turning top left")
            #animation
            direction = "topLeft/TL"
            #position change
            dx = - 5
            dy = 7
            self.flip = False
            
                 
        elif topRight and farRight:
            print("Turning far right")
            #animation
            direction = "farLeft/FL"
            #position change
            dx = 10
            dy = 5
            self.flip = True

        elif topRight or farRight: # xor: small turn
            print("Turning top right")
            #animation
            direction = "topLeft/TL"
            #position change
            dx = 5
            dy = 7
            self.flip = True

        else: # running straight
            print("Running straight")
            #animation
            direction = "straight/S"
            #position change
            dx = 0
            dy = 10
            self.flip = False

        #self.size = [scale * d for d in self.size]
        for frame in range(1,7):
            #redraw background
            for i in range(5):
                leaves.draw(screen)
                tree.scroll(4)
                tree.draw(screen)

                if (self.position[0] < 80 and dx < 0) or (self.position[0] > 480 and dx > 0):
                    direction = "straight/S"
                    dx = 0
                    dy = 5
                    self.flip = False
                
                self.path = f'assets/{direction}{frame}.png'
                self.position[0] += dx//5
            
                self.load_image()
                screen.blit(self.image, self.position)
                pygame.display.flip()
                

            

            #update lizard position and image
            #self.path = f'assets/{direction}{frame}.png'
            #self.position[0] += dx
            
            
            #self.position[1] += dy

            #self.load_image()
            #screen.blit(self.image, self.position)
            #pygame.display.flip()
            #pygame.time.delay(10)  # Delay to control the speed of the turn

           



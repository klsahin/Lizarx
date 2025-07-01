import pygame

class Background:
    def __init__(self, width, height, path1 = "assets/background1", path2 = "assets/background2"):
        self.position = [0, 0]
        self.size = [width, height]
        self.imagePath1 = path1
        self.imagePath2 = path2
        self.image1 = None
        self.image2 = None
        self.x_offset = 0

    def load_image(self):
        self.image1 = pygame.image.load(self.imagePath1).convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, self.size)
        self.image2 = pygame.image.load(self.imagePath2).convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, self.size)

    def draw(self, screen):
        # Draw two backgrounds side by side for endless effect
        w = self.size[0]
        x = -self.x_offset % w
        screen.blit(self.image1, (x, 0))
        screen.blit(self.image2, (x + w, 0))
        # If x > 0, draw the second background before the first
        if x > 0:
            screen.blit(self.image2, (x - w, 0))

    def scroll(self, dx):
        self.x_offset += dx

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
        pass


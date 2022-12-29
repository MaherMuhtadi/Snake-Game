# A simple Game Development Module using Python's Pygame library

import pygame
pygame.init()


class sprite():
    '''A game sprite class'''
    
    def __init__(self, image_path : str, initial_x : float = 0, initial_y : float = 0) -> None:
        '''Takes in string image path and initial floating-point coordinates of the sprite
           and creates an instance of the sprite'''
        self.image = pygame.image.load(image_path)
        self.image_collection = {"default" : self.image}
        self.position = pygame.math.Vector2(initial_x, initial_y)
        self.initial_position = pygame.math.Vector2(initial_x, initial_y)
    
    def update_position(self, new_x : float = None, new_y : float = None) -> None:
        '''Takes in new floating-point coordinates and updates the sprite's position'''
        if new_x != None:
            self.position.x = new_x
        if new_y != None:
            self.position.y = new_y
    
    def change_postion(self, x_change : float = None, y_change : float = None) -> None:
        '''Takes in floating-point changes in coordinates and updates the sprite's position'''
        if x_change != None:
            self.position.x += x_change
        if y_change != None:
            self.position.y += y_change
    
    def add_image(self, key : str, image_path : str) -> None:
        '''Takes in a string key and new string image path
           and adds the image of the sprite to the image_collection dictionary'''
        self.image_collection[key] = pygame.image.load(image_path)
    
    def change_image(self, key : str) -> None:
        '''Takes in the string key of image path and changes the image of the sprite accordingly'''
        self.image = self.image_collection[key]
    
    def rectangle(self, width : int, height : int) -> pygame.Rect:
        '''Takes in integer width and height and returns the sprite's rectangular hitbox'''
        return pygame.Rect(self.position.x, self.position.y, width, height)
    
    def reset(self) -> None:
        '''Resets the sprite object'''
        self.update_position(self.initial_position.x, self.initial_position.y)
        self.change_image("default")

    def draw(self, screen : pygame.Surface) -> None:
        '''Takes a screen of type Surface and draws the sprite on the screen'''
        screen.blit(self.image, (self.position.x, self.position.y))


class game():
    '''A game class'''

    def __init__(self, title : str = "Game Window",
                 window_size : tuple[int, int] = (800, 600),
                 color : tuple[int, int, int] = (0, 0, 0),
                 background_path : str = None,
                 icon_path : str = None,
                 bg_music_path : str = None,
                 fps : int = 100) -> None:
        '''Creates a game window based on the provided arguments'''
        self.title = title
        self.window_size = window_size
        self.background_color = color
        self.background = pygame.image.load(background_path) if background_path != None else None
        self.icon = pygame.image.load(icon_path) if icon_path != None else None
        self.bg_music_path = bg_music_path
        self.held_keys = pygame.key.get_pressed()
        self.sprites = []
        self.tasks = []
        self.event_tasks = []
        self.end_tasks = []
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = False
    
    def add_entity(self, sprite : sprite) -> None:
        '''Takes an object implementing class sprite and adds it to the list of game sprites'''
        self.sprites.append(sprite)
    
    def add_task(self, task):
        '''A decorator that adds a function to the list of game tasks'''
        self.tasks.append(task)
        return task
    
    def add_event_task(self, event_task):
        '''A decorator that adds a function which takes in game event as argument to the list of game event tasks'''
        self.event_tasks.append(event_task)
        return event_task
    
    def add_end_task(self, end_task):
        '''A decorator that adds a function to the list of game end tasks'''
        self.end_tasks.append(end_task)
        return end_task
    
    def clear_all(self) -> None:
        '''Clears all the game entities and tasks except for end tasks'''
        self.sprites = []
        self.tasks = []
        self.event_tasks = []

    def quit(self) -> None:
        '''Quits the game window'''
        self.clear_all()
        self.running = False

    def run(self) -> None:
        '''Runs the game'''
        pygame.display.set_caption(self.title)
        if self.icon != None:
            pygame.display.set_icon(self.icon)
        self.screen = pygame.display.set_mode(self.window_size)
        if self.bg_music_path != None:
            pygame.mixer.music.load(self.bg_music_path)
            pygame.mixer.music.play(-1)
        
        # Game loop
        self.running = True
        while self.running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                # Quits the game
                if event.type == pygame.QUIT:
                    self.quit()
                
                for event_task in self.event_tasks:
                    event_task(event)
            
            # Sets the background
            if self.background == None:
                self.screen.fill(self.background_color)
            else:
                self.screen.blit(self.background, (0, 0))
            
            # Updates the pressed keys
            self.held_keys = pygame.key.get_pressed()
            
            # Handles the tasks
            for sprite in self.sprites:
                sprite.draw(self.screen)
            for task in self.tasks:
                task()
            
            pygame.display.update()
        
        # Handles tasks upon quitting the game
        for end_task in self.end_tasks:
            end_task()
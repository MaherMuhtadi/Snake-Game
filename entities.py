from game_module import *
import random


class food(sprite):
    '''A class containing the behavior of the food'''

    def __init__(self, image_path: str, initial_x: float, initial_y: float, window_size : tuple) -> None:
        '''Takes in string image path and initial floating-point coordinates of the food
           and creates an instance of the food'''
        super().__init__(image_path=image_path, initial_x=initial_x, initial_y=initial_y)
        self.window_width = window_size[0]
        self.window_height = window_size[1]
    
    def respawn(self) -> None:
        '''Spawns a new food by randomly updating the food's position.'''
        super().update_position(random.randint(0, self.window_width-32), random.randint(0, self.window_height-32))


class snake(sprite):
    '''A class containing the behavior of the snake'''

    def __init__(self, head_image_paths : dict[str:str], body_image_path : str, tail_image_paths : dict[str:str],
                 initial_x: float, initial_y: float, food : food, window_size : tuple, 
                 eat_audio : pygame.mixer.Sound = None, death_audio : pygame.mixer.Sound = None) -> None:
        '''Creates the immature snake using the provided arguments'''
        # Creating the body parts
        head = sprite(image_path=head_image_paths["r"], initial_x=initial_x, initial_y=initial_y)
        self.body_image_path = body_image_path
        body = sprite(image_path=body_image_path, initial_x=initial_x-16, initial_y=initial_y)
        tail = sprite(image_path=tail_image_paths["r"], initial_x=initial_x-32, initial_y=initial_y)
        for key in head_image_paths:
            head.add_image(key, head_image_paths[key])
        for key in tail_image_paths:
            tail.add_image(key, tail_image_paths[key])
            
        self.parts = [tail, body, head]
        self.initial_parts = self.parts.copy()
        self.part_directions = ["r", "r", "r"]
        self.x_change, self.y_change = 16, 0
        self.food = food
        self.window_size = window_size
        self.still = False
        self.eat_audio = eat_audio
        self.death_audio = death_audio
    
    def movement_toggle(self) -> None:
        '''Toggles the snake's movement'''
        if not self.still:
            self.still = True
        else:
            self.still = False
    
    def key_press_detection(self, event) -> None:
        '''Detects key presses'''
        if not self.still and event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w) and self.part_directions[-2] in ("r", "l"):
                self.x_change, self.y_change = 0, -16
                self.part_directions[-1] = "u"
            if event.key in (pygame.K_DOWN, pygame.K_s) and self.part_directions[-2] in ("r", "l"):
                self.x_change, self.y_change = 0, 16
                self.part_directions[-1] = "d"
            if event.key in (pygame.K_RIGHT, pygame.K_d) and self.part_directions[-2] in ("u", "d"):
                self.x_change, self.y_change = 16, 0
                self.part_directions[-1] = "r"
            if event.key in (pygame.K_LEFT, pygame.K_a) and self.part_directions[-2] in ("u", "d"):
                self.x_change, self.y_change = -16, 0
                self.part_directions[-1] = "l"

    def move(self) -> None:
        '''Moves the snake'''
        if not self.still:
            for i in range(len(self.parts)-1):
                self.parts[i].update_position(self.parts[i+1].position.x, self.parts[i+1].position.y)
                self.part_directions[i] = self.part_directions[i+1]
            self.parts[-1].change_postion(self.x_change, self.y_change)
                
            # Changing the head and tail directions
            self.parts[-1].change_image(self.part_directions[-1])
            self.parts[0].change_image(self.part_directions[0])
    
    def eat(self) -> bool:
        '''Eating event, returns True when the snake eats and False otherwise'''
        ate = False

        if self.parts[-1].rectangle(16, 16).colliderect(self.food.rectangle(32, 32)):
            ate = True
            if self.eat_audio != None:    
                self.eat_audio.play()

            # Grows the snake
            new_body_segment = sprite(image_path=self.body_image_path, 
                                      initial_x=self.parts[-1].position.x, 
                                      initial_y=self.parts[-1].position.y)
            self.parts.insert(-1, new_body_segment)
            self.part_directions.insert(-1, self.part_directions[-1])
            self.parts[-1].change_postion(self.x_change, self.y_change)

            # Respawns the food on unoccupied grounds, if there is a clash, it respawns elsewhere
            occupied_rectangles = [part.rectangle(16, 16) for part in self.parts]
            clash_check = [part.colliderect(self.food.rectangle(32, 32)) for part in occupied_rectangles]
            while True in clash_check:
                self.food.respawn()
                clash_check = [part.colliderect(self.food.rectangle(32, 32)) for part in occupied_rectangles]
        
        return ate
    
    def death(self) -> bool:
        '''Death event, returns True when the snake dies and False otherwise'''
        died = False

        # Eating itself
        part_rectangles = [part.rectangle(16, 16) for part in self.parts]
        for part in part_rectangles[:-1]:
            if part_rectangles[-1].colliderect(part):
                died = True
                
        # Crossing the boundary
        if self.y_change == 0 and (self.parts[-1].position.x < 0 or self.parts[-1].position.x > self.window_size[0]-16):
            died = True
        if self.x_change == 0 and (self.parts[-1].position.y < 0 or self.parts[-1].position.y > self.window_size[1]-16):
            died = True
        
        if died and self.death_audio != None:
            self.death_audio.play()
        
        return died
    
    def reset(self) -> None:
        '''Resets the snake object'''
        self.parts = self.initial_parts.copy()
        for part in self.parts:
            part.reset()
        self.part_directions = ["r", "r", "r"]
        self.x_change, self.y_change = 16, 0
        self.food.reset()

    def draw(self, screen: pygame.Surface) -> None:
        '''Takes a screen of type Surface and draws the snake on the screen.'''
        for part in self.parts:
            part.draw(screen)
from game_module import *
from entities import snake

class game_state():
    '''A class handling the game state'''

    def __init__(self, game : game, snake : snake, font_path : str, text_sizes : tuple[int,int], record_path : str,
                 color_1 : tuple, color_2 : tuple) -> None:
        '''Creates an instance of the class'''
        self.start = True
        self.snake = snake
        self.game = game
        self.background = game.background
        self.window_width = game.window_size[0]
        self.window_height = game.window_size[1]
        self.small_font = pygame.font.Font(font_path, min(text_sizes))
        self.large_font = pygame.font.Font(font_path, max(text_sizes))
        self.color_1 = color_1
        self.color_2 = color_2
        
        self.score = 3
        self.record_path = record_path
        try:
            saved_record = open(record_path, "r")
            self.record = int(saved_record.read())
            saved_record.close()
        except:
            self.record = 3
    
    def begin(self) -> None:
        '''Starts the game upon pressing ENTER key'''
        if self.start:
            self.game.screen.blit(self.background, (0, 0))
            credit_text = self.small_font.render("Created by Maher Muhtadi", True, self.color_2)
            credit_text_size = self.small_font.size("Created by Maher Muhtadi")
            space = credit_text_size[1]/2
            begin_text = self.large_font.render("Press ENTER to begin", True, self.color_1)
            begin_text_size = self.large_font.size("Press ENTER to begin")
            self.game.screen.blit(credit_text, ((self.window_width-credit_text_size[0])/2, self.window_height-3*space))
            self.game.screen.blit(begin_text, ((self.window_width-begin_text_size[0])/2, (self.window_height-begin_text_size[1])/2))
            pygame.display.update()
        
        # Displays press ENTER message until either ENTER is pressed or the game is quit
        while self.start:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.start = False
                elif event.type == pygame.QUIT:
                    self.game.quit()
                    self.start = False
    
    def pause(self, event) -> None:
        '''Toggles pause'''
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.snake.movement_toggle()
            if self.snake.still:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
    
    def paused_message(self) -> None:
        '''Displays the Paused message when game is paused'''
        if self.snake.still:
            text = self.large_font.render("Paused", True, self.color_1)
            text_size = self.large_font.size("Paused")
            self.game.screen.blit(text, ((self.window_width-text_size[0])/2, (self.window_height-text_size[1])/2))
    
    def score_handler(self) -> None:
        '''Handles the score and record'''
        # Updates the score and record
        if self.snake.eat():
            self.score += 1
            if self.score > self.record:
                self.record = self.score

        # Displays the score and record
        score_text = self.small_font.render("Length: "+str(self.score), True, self.color_2)
        score_text_size = self.small_font.size("Length: "+str(self.score))
        space = score_text_size[1]/2
        record_text = self.small_font.render("Record: "+str(self.record), True, self.color_2)
        record_text_size = self.small_font.size("Record: "+str(self.record))
        if self.snake.parts[-1].position.y > self.window_height/2:
            self.game.screen.blit(score_text, (space, space))
            self.game.screen.blit(record_text, (self.window_width-space-record_text_size[0], space))
        else:
            self.game.screen.blit(score_text, (space, self.window_height-3*space))
            self.game.screen.blit(record_text, (self.window_width-space-record_text_size[0], self.window_height-3*space))
    
    def game_over(self) -> None:
        '''Displays Game Over message and restarts the game upon pressing enter'''
        if self.snake.death():
            over_text = self.large_font.render("Game Over", True, self.color_1)
            over_text_size = self.large_font.size("Game Over")
            replay_text = self.small_font.render("Press ENTER to replay", True, self.color_2)
            replay_text_size = self.small_font.size("Press ENTER to replay")
            self.game.screen.blit(over_text, ((self.window_width-over_text_size[0])/2, (self.window_height-over_text_size[1]-replay_text_size[1])/2))
            self.game.screen.blit(replay_text, ((self.window_width-replay_text_size[0])/2, (self.window_height+over_text_size[1]-replay_text_size[1])/2))
            pygame.display.update()
            pygame.mixer.music.stop()
            over = True
            while over:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.snake.reset()
                        self.score = 3
                        pygame.mixer.music.play(-1)
                        over = False
                    elif event.type == pygame.QUIT:
                        self.game.quit()
                        over = False

    def save(self) -> None:
        '''Updates the record in the save file'''
        saved_record = open(self.record_path, "w")
        saved_record.write(str(self.record))
        saved_record.close()
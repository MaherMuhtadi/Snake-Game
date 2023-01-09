from game_module import *
from entities import food, snake
from game_state import game_state

# Creating the snake game
snake_game = game(title="Snake",
                  window_size=(560, 560),
                  background_path=r"images/background.png",
                  icon_path=r"images/icon.ico",
                  bg_music_path=r"audio/music.mp3",
                  fps=10)

# Loading the sound effects
score_mp3 = pygame.mixer.Sound(r"audio/score.mp3")
death_mp3 = pygame.mixer.Sound(r"audio/death.mp3")

# Adding the mouse to the game
mouse = food(image_path=r"images/mouse.png", initial_x=384, initial_y=264, window_size=snake_game.window_size)
snake_game.add_entity(mouse)

# Storing the snake head and tail image paths
head_image_paths = {"r":r"images/head_right.png", "l":r"images/head_left.png", "u":r"images/head_up.png", "d":r"images/head_down.png"}
tail_image_paths = {"l":r"images/tail_right.png", "r":r"images/tail_left.png", "d":r"images/tail_up.png", "u":r"images/tail_down.png"}

# Adding the snake to the game
snake = snake(head_image_paths=head_image_paths, body_image_path=r"images/body.png", tail_image_paths=tail_image_paths,
              initial_x=160, initial_y=272, food=mouse, window_size=snake_game.window_size, eat_audio=score_mp3, death_audio=death_mp3)
snake_game.add_entity(snake)

# Game state object
state = game_state(game=snake_game, snake=snake, font_path=r"font.ttf", text_sizes=(16, 32), 
                   record_path=r"record.txt", color_1=(255, 201, 14), color_2=(255, 255, 255))

# Adding the game functions
snake_game.add_event_task(state.pause)
snake_game.add_event_task(snake.key_press_detection)
snake_game.add_task(state.begin)
snake_game.add_task(state.paused_message)
snake_game.add_task(snake.move)
snake_game.add_task(state.score_handler)
snake_game.add_task(state.game_over)
snake_game.add_end_task(state.save)

snake_game.run()
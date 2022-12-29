<div align="center">

# Snake

</div>

## Description
This is a version of the Snake game programmed with Python using my [Python Game Development Module](https://github.com/MaherMuhtadi/Python-Game-Development-Module) and the [PyGame](https://www.pygame.org/docs/) library. The game can only run on the Windows OS.

This project was my attempt at simple 2-D game development using object oriented programming. In addition, I used it to help build my game development module and demonstrate its application.

### Features
1. The snake can move around the screen using the arrow keys or <kbd>w</kbd>, <kbd>a</kbd>, <kbd>s</kbd>, <kbd>d</kbd> keys.
2. The snake grows in length every time it devours a mouse by colliding with it.
3. After a mouse is devoured, a new one spawns at a random location on the field.
4. The game can be paused and resumed using the <kbd>esc</kbd> key.
5. The game ends and if the snake touches the edge of the screen or its own body part.
6. The player has the option to replay the game after it is over by pressing the <kbd>enter</kbd> key.
7. The game can track and display the snake's length and the highest length so far. The highest length is updated in an external text file every time the game window is quit.

## Installation
Make sure you follow the steps and run the program on a Windows machine.

### Prerequisites
1. Download and install the latest version of [Python](https://www.python.org/downloads/) that is compatible with [PyGame](https://www.pygame.org/wiki/GettingStarted).
2. Check if python is properly installed along with its package installer using the following commands in your terminal:
```
$ python --version
$ python -m pip --version
```
3. If the Python package installer, pip, is not installed, get it installed using the [pip documentation](https://pip.pypa.io/en/stable/getting-started/).
4. Install the PyGame module by running the following command in your terminal:

    `pip install pygame`

### Usage
1. Download the repository as a ZIP or [clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) the repository to your local device.
2. On your terminal, change directory to the repository folder using the `cd` command.
3. Run the `main.py` file using the command:

    `python main.py`
---
Last Updated: December 29, 2022
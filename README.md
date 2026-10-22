# Random Shape Generator
Note: This is my Final Project for Code In Place 2026 

This is a fun and interactive Python application built with the Pygame library. It generates a wide variety of colorful shapes on your screen based on your keyboard and mouse inputs. 

## Features

* **Various Shapes:** Creates over 20 different types of shapes, including circles, stars, hearts, clouds, spirals, and waves.
* **Interactive Controls:** Add shapes by pressing numbers on your keyboard or clicking your mouse.
* **Cooldown System:** Includes a 0.3-second wait time between inputs to prevent spamming, complete with visual feedback on the screen.
* **Smart Limit:** Automatically removes the oldest shapes when the screen reaches the maximum limit (400 shapes) to keep the performance smooth.
* **Graceful Exit:** Pressing the Spacebar starts a clean 3-second countdown animation before closing the application.

## Requirements

To run this project, you need to have Python installed on your computer along with the Pygame library.

You can install Pygame using pip:

```bash
pip install pygame
```

## Controls

| Input | Action |
|---|---|
| **Keys 1-9** | Adds shapes to the screen. The number of shapes matches the key you press. |
| **Left Mouse Click** | Instantly adds multiple shapes at once (10 shapes by default). |
| **Spacebar** | Starts a 3-second countdown to exit the program safely. |

## How to Run

1. Make sure you have installed Pygame.
2. Save the code in a file, for example, `shapes.py`.
3. Open your terminal or command prompt.
4. Run the script using the following command:

```bash
python shapes.py
```

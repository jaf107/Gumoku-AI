# Gumoku AI

Welcome to Gumoku AI! This repository contains the project developed for the AI course, focused on building an Artificial Intelligence agent to play the game Gumoku. Gumoku is a variant of the popular game Gomoku (also known as Five in a Row), played on a Go board.

## Game Description

Gumoku is a two-player strategy board game where the objective is to be the first to align five of your pieces in a row, either horizontally, vertically, or diagonally. Players take turns placing their pieces on an empty cell of the board until one player achieves the winning condition.

## Requirements

- Python 3.x

## Dependencies

The Gumoku AI project relies on the following Python libraries:

- numpy: Used for efficient array operations and board representation.
- pygame: Used for creating a simple GUI to play against the AI.

## Installation

To run the Gumoku AI project on your local machine, follow these steps:

1. Make sure you have Python 3.x installed. If you don't have it, you can download it from the official website: https://www.python.org/downloads/

2. Clone this repository to your local machine using git or download it as a ZIP file and extract it.

3. Open a terminal or command prompt, navigate to the project's directory, and create a virtual environment (optional but recommended).

4. Install the project dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```

## How to Play

To play Gumoku against the AI, execute the `gumoku.py` file in your Python environment:

```
python gumoku.py
```

The game will start, and you will be presented with a graphical user interface where you can interact with the board. The AI will make its moves automatically after you make yours.

To place a piece, click on the desired cell of the board. The AI will then take its turn and place its piece on the board as well. Continue taking turns until one player wins or the game ends in a draw.

## AI Algorithm

The Gumoku AI is based on a specific algorithm (mention the algorithm if known, like Minimax with Alpha-Beta Pruning or Monte Carlo Tree Search) to make strategic decisions during its turn. The algorithm has been implemented in the `gumoku_ai.py` file.

## Contribution

We welcome contributions to the Gumoku AI project! If you find any issues, or bugs, or have ideas for improvements, please feel free to open an issue or submit a pull request.

## Collaborators

- Abu Jafar Saifullah: bsse1109@iit.du.ac.bd
- Jitesh Sureka: bsse1115@iit.du.ac.bd

## License

This project is licensed under the MIT License. You can find the details in the `LICENSE` file.

## Acknowledgments

We would like to thank all contributors to this project and the AI course instructors for their guidance and support.

Have fun playing Gumoku against the AI!

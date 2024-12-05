# Quantum Wordle: A Quantum Computing Word-Guessing Game

🚀 **Quantum Wordle** combines the mechanics of a word-guessing game with the power of quantum computing. Using Qiskit, custom quantum circuits, and Grover’s Algorithm, this project probabilistically identifies correct letters, making it a fun and educational way to explore quantum principles.

## Features
- Implements **Grover’s Algorithm** to efficiently search for correct letters.
- Uses **quantum circuits** to generate probabilistic feedback based on player guesses.
- Demonstrates quantum principles like **superposition** and **measurement probabilities**.

## How It Works
Players guess letters of a hidden word, and the game evaluates:

1. Correct letters in the *correct* positions.
2. Correct letters in *incorrect* positions.
3. Letters not present in the hidden word.

Custom quantum circuits adjust measurement probabilities to provide feedback, while Grover’s Algorithm amplifies the likelihood of finding correct letters.

## Explore the Project
To dive deeper into the quantum mechanics, code implementation, and educational insights, check out the [Jupyter Notebook]([link](https://github.com/matttavares9/quantum-wordle/blob/main/quantum_wordle_demo.ipynb)).

## Technologies Used
- Python
- Qiskit
- Jupyter Notebook

## Why This Project?
This project gamifies quantum computing, offering a hands-on way to learn concepts like superposition, measurement probabilities, and quantum optimization in an engaging format.

## Get Started
1. Clone the repository: `git clone <repo-link>`
2. Navigate to the project directory: `cd quantum-wordle`
3. Open the Jupyter Notebook: `jupyter notebook quantum_wordle_demo.ipynb`
4. Play the game: `python main.py`

Enjoy exploring quantum computing through the Quantum Wordle game!

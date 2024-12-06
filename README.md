# Quantum Wordle: A Quantum Computing Word-Guessing Game

🚀 **Quantum Wordle** combines the mechanics of a word-guessing game with the power of quantum computing. Using Qiskit, custom quantum circuits, and Grover’s Algorithm, this project probabilistically identifies correct letters, making it a fun and educational way to explore quantum principles.

## Features
- Implements **Grover’s Algorithm** to efficiently search for correct letters.
- Uses **quantum circuits** to generate probabilistic feedback based on player guesses.
- Demonstrates quantum principles like **superposition** and **measurement probabilities**.

## How It Works
Players guess letters of a hidden word, and custom quantum circuits analyze their guesses to provide probabilistic feedback.


| Feedback Type                   | Probability        | Example Output       |
|---------------------------------|--------------------|----------------------|
| **Correct letters, correct positions** | ~50% chance correct letter is measured | `A` (uppercase)       |
|                                 | ~50% chance another letter in the word is measured | `b` (lowercase)       |
| **Correct letters, incorrect positions** | ~50% chance letter is measured         | `c` (lowercase)       |
|                                 | ~25% chance letter in the word is measured | `A` (uppercase) or `b` (lowercase)      |
|                                 | ~25% chance a random letter is measured    | `x` (lowercase)       |
| **Letters not in the word**     | Equal chance for any random letter         | `x` (lowercase)       |


Custom quantum circuits adjust measurement probabilities to provide feedback, while Grover’s Algorithm amplifies the likelihood of finding correct letters.

## Explore the Project
To dive deeper into the quantum mechanics, code implementation, and educational insights, check out the [Jupyter Notebook](https://github.com/matttavares9/quantum-wordle/blob/main/quantum_wordle_demo.ipynb).

## Technologies Used
- Python
- Qiskit
- Jupyter Notebook

## Why This Project?
This project gamifies quantum computing, offering a hands-on way to learn concepts like superposition, measurement probabilities, and quantum optimization in an engaging format.

## Get Started
1. Clone the repository: `git clone <repo-link>`
2. Install [Qiskit](https://docs.quantum.ibm.com/guides/install-qiskit): `pip install qiskit`
3. Navigate to the project directory: `cd quantum-wordle`
4. Open the Jupyter Notebook: `jupyter notebook quantum_wordle_demo.ipynb`
5. Play the game: `python main.py`

Enjoy your quantum gaming experience!

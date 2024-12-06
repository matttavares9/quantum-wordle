from qiskit_aer.primitives import SamplerV2
from qiskit import QuantumCircuit
import math
import random
import string

class QuantumWordle:
    def __init__(self, hidden_word):
        if len(hidden_word) != 5:
            raise ValueError("Input must be a 5 letter word!")
        if all(c.isalpha() for c in hidden_word) == False:
            raise ValueError("Input must only have letters!")
        
        self.hidden_word = hidden_word.upper()

        """ Initialize the solution space for each letter in the hidden word. """
        self.word_solution_space = {
            self.hidden_word[0]:'000',
            self.hidden_word[1]:'001',
            self.hidden_word[2]:'010',
            self.hidden_word[3]:'011',
            self.hidden_word[4]:'111'
        }

        """ Initialize a mapping for all 32 qubit states to empty letter values. """
        states = [f'{i:05b}' for i in range(32)]
        self.state_to_letter = {state: '' for state in states}

        """ Initialize a map for each letter of the guess to a state position. """
        self.guess_to_state = {}

        """ List storing all guesses entered. """
        self.all_output_guesses = []

        self.reset()

    def reset(self):
        """ Set random value for each of the 32 qubit states """

        all_letters = list(string.ascii_uppercase)
        for state in self.state_to_letter:
            index = random.randint(0, 25)
            self.state_to_letter[state] = all_letters[index] #Each qubit is a random letter in the word
    
    def guess(self, guess):
        """ Updates the and begins grovers_search """

        self.guess_to_state = {
            guess[0]:'000',
            guess[1]:'001',
            guess[2]:'010',
            guess[3]:'011',
            guess[4]:'111'
        }

        return self.grovers_search(guess)

    def grovers_search(self, guess):
        """ Grover's Search Algorithm: 
            
            For each letter in the guessed word:
                - The letter is marked by oracle.
                - Letter is searched for in a superposition of all letter states in the hidden word.
                - Qubit measurements are returned, where it's mapping determines wether the letter is in:
                    1. Correct position
                    2. Incorrect position
                    3. Incorrect letter

            Time complexity: 
                O(√N*N) which is a theoretical speedup from a classical O(N^2)
            
            Potential future plans: 
                With more qubits, this could be done where the entire word is searched for in a 
                superposition of all possible words. """

        """ (1) Create superposition of all possible letters """
        N = 2
        circuit = QuantumCircuit(N+1) # 2^2 + 1 = 5 (2 in superposition and 1 ancilla).

        """ Notation: |0 0 0 >
                       ^ ^ ^
                       | | |
               Qubit:  2 1 0  """

        # Only first 3 qubits in Hadamard, as 2^3 = 8 total in solution space.
        circuit.h([0,1])

        # List of tuples containing the letter and its corresponding state measured.
        letter_position = []

        def U_f(letter):
            """ (2) Oracle U_f:

                If all qubits are in state |1>, rotate phase by pi (Z rotation). 

                Controlled Z gates are applied to flip phase of |11111> to -|11111>, 
                marking it as the "winner state". Then, X gates are applied as
                needed, to revert it back to the state corresponding to its letter. """
            
            # The qubit mapped to the letter to be marked.
            state = self.word_solution_space.get(letter)

            if state == '000':
                circuit.cz(0, 1)
                circuit.x([0,1]) 
            elif state == '001':
                circuit.cz(0, 1)
                circuit.x([1])
            elif state == '010':
                circuit.cz(0, 1)
                circuit.x([0])
            elif state == '011': 
                circuit.cz(0, 1)
            elif state == '111':
                circuit.cz(0, 1)
                circuit.x(2)

        def U_s():
            """ (3) Diffuser U_s:

                2|s><s| - I, which is a REFLECTION about the |s> axis (mean of all states) 
                towards the winning state.This increases the probability of measuring the 
                winning state. """
            
            circuit.h([0, 1])
            circuit.z([0,1])
            circuit.cz(0, 1)
            circuit.h([0,1])
        
        def measure(letter):
            """ (4) Measure the qubits: """

            circuit.measure_all()

            # Simulate on a Quantum Simulator, SamplerV2.
            sampler = SamplerV2()
            job = sampler.run([circuit], shots=200)
            result_ideal = job.result()
            counts_ideal = result_ideal[0].data.meas.get_counts()
            
            # Sort all the states measured and place them in list.
            sorted_counts = dict(sorted(counts_ideal.items(), key=lambda item: item[1], reverse=True))
            collapsed_states = list(sorted_counts.keys())

            # Update letter_position to contain: letter, states measured.
            letter_position.append((letter,collapsed_states))
        
        """ (5) Grover iterator:
        
            Only need to repeat Grover's oracle and diffuser one time, as 1/pi * sqrt(2) < 1.
            Diffuser will reflect the state immediately to the winning state (if winning state
            exists).

            Time complexity:
                O(√N*N) rather than O(N^2) """
        
        grover_iterations = ( math.pi / 4 ) * ( math.sqrt(N) )
        for n in range(len(guess)): # N iterations
            letter = guess[n]
            for t in range(math.floor(grover_iterations)): # √N iterations
                U_f(letter)
                U_s()
            measure(letter)

            # Reset circuit for next letter
            circuit = QuantumCircuit(N+1)
            circuit.h([0,1])

        return self.quantum_feedback(letter_position)

    def quantum_feedback(self, letters_position):
        """ Method to evaluate the accuracy of the guess with quantum game mechanics.
            
            For each letter, state pair in letters_position, if:

            1. Correct Letter, Correct Position:
                - ~50% chance correct letter is revealed with an uppercase letter.
                - ~50% chance another letter in the hidden word is revealed with *lowercase* 
                  letter and an aesteric to provide the user with the hint.
            2. Correct Letter, Wrong Position:
                - ~50% chance letter is revealed with a lowercase letter.
                - ~25% chance letter in word is revealed with an uppercase letter.
                - ~25% chance a random letter is revealed with a lowercase letter.
            3. Incorrect Letter:
                - A random letter of equal probability with a lowercase letter. """
        
        quantum_output = ["","","","",""] # Stores feedback with quantum effects.

        i = 0
        for letter, states in letters_position:

            theta = 0 # Theta value input into the quantum circuit.
            feedback = ""
            
            """ If the state found by Grover's search is the same state as the letter, then
                it is the correct letter in the correct position.

                This is because the order of the states are the same for both mappings,
                therefore representing the letters' positions. """
            is_correct_position = self.guess_to_state.get(letter) == states[0]

            if len(states) > 1: 
                """ If Grover's search measures multiple states, then it didn't mark/contain
                    the letter.

                    Leaves theta = 0, to display a random trick letter. """
                pass 
            elif is_correct_position is True:
                """ Correct letter in correct position """

                """Set letter to state |1111>. This has a ~50% chance of being measured
                    on the circuit. """
                temp = self.state_to_letter.get('11111')
                self.state_to_letter['11111'] = letter
                self.state_to_letter[self.state_to_letter.get(letter)] = temp

                """ Set other letter in the hidden word to the following states. Measuring
                    one of these has a 50% chance on the circuit. """
                other_states = ["11110","11100", "11000", "10000", "00000"]
                for state in other_states:
                    index = random.randint(0, 4)
                    self.state_to_letter[state] = self.hidden_word[index] #Each qubit is a random letter in the word
                
                """ Value of theta is updated to math.pi/2.

                    When ran on the circuit, the CRY gates eliminate the |01> state, thus there are 
                    only 3 possible states |00>, |01>, |10> (see Jupyter Notebook) for 2 qubits.

                    Purpose: For 5 qubits, it reduces number of states to only 6 (does not contain |01>)
                    which can be easily mapped to 5 (plus 1 random) letter in the word - each with an
                    approximately equal amplitude. Most importantly, it amplifies the probability of 
                    measuring state |1111> the highest, which is mapped to the letter. """
                theta = math.pi/2
            else: 
                """ Correct letter in incorrect position"""

                """ Set letter to state |1111>. This has a ~50% chance of being measured
                    on the circuit. """
                temp = self.state_to_letter.get('11111')
                self.state_to_letter['11111'] = str(letter)
                self.state_to_letter[self.state_to_letter.get(letter)] = temp

                """ Set other letter in the hidden word to the following states. Measuring
                one of these has a 50% chance on the circuit. """
                other_states = ["11110","11100", "11000", "10000", "00000"]
                for state in other_states:
                    index = random.randint(0, 4)
                    self.state_to_letter[state] = self.hidden_word[index]
            
                """ Value of theta is updated to 2*math.pi/3.

                    Purpose: When ran on the circuit, state |11111> has a ~50% chance of being measured,
                    which corresponds to the guessed letter. However, the states |11110>,|11100>, |11000>, 
                    |10000> and |00000> have a ~25% of being measured, which correspond to a random letter
                    in the hidden word.
                    
                    The remaining states have also a ~25% of being measured, which correspond to a random
                    "trick" letter in the alphabet already set in self.state_to_letter. """

                theta = 2*math.pi/3

            """ Get a state corresponding to a letter in the alphabet based on theta. """
            state = self.CRY_gates(theta)

            """ Feedback is the letter mapped to state. """
            feedback+=self.state_to_letter.get(str(state))

            if (letter == self.hidden_word[i]) and (feedback != letter):
                feedback = feedback.lower()
            elif feedback != self.hidden_word[i]:
                # Reveal as letter as lowercase to show incorrect position.
                feedback = feedback.lower()
            quantum_output[i] = feedback
            i+=1

        # Reset state_to_letter back to random state, letter pairs.
        self.reset()
        guess = ''.join([letter for letter, _ in letters_position[:5]])

        # Reveal the hints to user.
        self.reveal(quantum_output)

        """ Returns back to main.py """
        if guess == self.hidden_word:
            print("You won!")
            return True
        return False

    def CRY_gates(self,theta):
        """ Controlled-Y Rotations on 5-Qubit Circuit:

            Depending on theta, the amplitude of measuring one of the 32 possible states 
            will change, with state |1111> having the greatest probability. """
        
        """ Construct circuit with 5 qubits, and apply Hadamard gates on each for
            2^5 = 32 possible states. """
        circ = QuantumCircuit(5)
        circ.h([0, 1, 2, 3, 4])

        """ If control qubit is in state |1>, it performs a Y-rotation of angle theta. 
            This directly alters the probability amplitudes of each qubit. """
        circ.cry(theta,[0],[1])
        circ.cry(theta,[1],[2])
        circ.cry(theta,[2],[3])
        circ.cry(theta,[3],[4])

        """ Measure the qubits. """
        circ.measure_all()

        """ Run on simulator. """
        sampler = SamplerV2()
        job = sampler.run([circ], shots=1)
        result_ideal = job.result()
        counts_ideal = result_ideal[0].data.meas.get_counts()
        measured_state = list(counts_ideal.items())[0][0]

        """ Returns measured state. """
        return measured_state

    def reveal(self, output):
        """ Display feedback to user for each collapsed letter."""

        x_perimeter = "+--+--+--+--+--+"
        y_perimeter = "|"

        self.all_output_guesses.append(output)

        for x in range(6):
            print(x_perimeter)
            for y in range(6):
                print(y_perimeter, end='')
                num_guesses = len(self.all_output_guesses)
                if x <= num_guesses-1:
                    curr_output = self.all_output_guesses[x]
                    if y < 5:
                        current_letter = curr_output[y]
                        print(current_letter + " ", end='')
                else:
                    print("  ", end = '')
            print()
        print(x_perimeter)
        print()
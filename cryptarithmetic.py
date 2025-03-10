import itertools
import time
from tabulate import tabulate

def solve_cryptarithmetic(words, result):
    """
    Solve a cryptarithmetic problem where words[0] + words[1] + ... = result
    """
    # Get all unique letters
    letters = set(''.join(words + [result]))
    
    # We can't have more than 10 unique digits (0-9)
    if len(letters) > 10:
        return None
    
    # Get first letters of all words (can't be zero)
    first_letters = {word[0] for word in words + [result]}
    
    # Try all possible digit assignments
    digits = range(10)
    
    total_attempts = 0
    start_time = time.time()
    
    # For better presentation, keep track of some attempts
    example_attempts = []
    
    for perm in itertools.permutations(digits, len(letters)):
        total_attempts += 1
        # Create a mapping from letters to digits
        letter_to_digit = dict(zip(letters, perm))
        
        # Check if any first letter is assigned 0
        if any(letter_to_digit[letter] == 0 for letter in first_letters):
            continue
        
        # Convert words to numbers
        numbers = []
        for word in words:
            number = 0
            for letter in word:
                number = number * 10 + letter_to_digit[letter]
            numbers.append(number)
        
        # Convert result to number
        result_number = 0
        for letter in result:
            result_number = result_number * 10 + letter_to_digit[letter]
        
        # Check if equation is satisfied
        if sum(numbers) == result_number:
            # Record some attempts for visualization
            if len(example_attempts) < 5:
                example_attempts.append((letter_to_digit.copy(), numbers, result_number, "SOLUTION!" if sum(numbers) == result_number else ""))
            
            end_time = time.time()
            
            # Return the solution and statistics
            return {
                "solution": letter_to_digit,
                "numbers": numbers,
                "result": result_number,
                "attempts": total_attempts,
                "time": end_time - start_time,
                "example_attempts": example_attempts
            }
        
        # Record some random attempts for visualization
        if total_attempts % 10000 == 1 and len(example_attempts) < 5:
            example_attempts.append((letter_to_digit.copy(), numbers, result_number, ""))
    
    end_time = time.time()
    return {
        "solution": None, 
        "attempts": total_attempts, 
        "time": end_time - start_time,
        "example_attempts": example_attempts
    }

def display_solution(problem_name, words, result, solution_data):
    print(f"\n{'=' * 60}")
    print(f"SOLVING {problem_name}: {' + '.join(words)} = {result}")
    print(f"{'=' * 60}")
    
    if solution_data["solution"]:
        print("✅ SOLUTION FOUND!")
        print("\nLetter assignments:")
        
        # Format letter assignments nicely
        letter_assignments = solution_data["solution"]
        letters = sorted(letter_assignments.keys())
        
        # Display letters
        print("  ", end="")
        for letter in letters:
            print(f"{letter} ", end="")
        print()
        
        # Display digits
        print("  ", end="")
        for letter in letters:
            print(f"{letter_assignments[letter]} ", end="")
        print("\n")
        
        # Show the equation with values
        for i, word in enumerate(words):
            print(f"{word} = ", end="")
            for letter in word:
                print(letter_assignments[letter], end="")
            print(f" = {solution_data['numbers'][i]}")
        
        print(f"{result} = ", end="")
        for letter in result:
            print(letter_assignments[letter], end="")
        print(f" = {solution_data['result']}")
        
        print(f"\n{' + '.join(str(num) for num in solution_data['numbers'])} = {solution_data['result']}")
    else:
        print("❌ NO SOLUTION FOUND")
    
    print(f"\nStatistics:")
    print(f"Total attempts: {solution_data['attempts']:,}")
    print(f"Time taken: {solution_data['time']:.3f} seconds")
    
    if solution_data["example_attempts"]:
        print("\nExample attempts:")
        table_data = []
        headers = ["Attempt", "Letter Assignments", "Equation", "Result"]
        
        for i, (letter_to_digit, numbers, result_num, note) in enumerate(solution_data["example_attempts"]):
            assignments = ", ".join(f"{letter}={letter_to_digit[letter]}" for letter in sorted(letter_to_digit.keys()))
            equation = f"{' + '.join(str(num) for num in numbers)} = {result_num}"
            status = "✓" if sum(numbers) == result_num else "✗"
            table_data.append([i+1, assignments, equation, f"{status} {note}"])
        
        print(tabulate(table_data, headers, tablefmt="grid"))

def main():
    # Problem 1: SEND + MORE = MONEY
    problem1_words = ["SEND", "MORE"]
    problem1_result = "MONEY"
    solution1 = solve_cryptarithmetic(problem1_words, problem1_result)
    display_solution("Problem 1", problem1_words, problem1_result, solution1)
    
    # Problem 2: BASE + BALL = GAMES
    problem2_words = ["BASE", "BALL"]
    problem2_result = "GAMES"
    solution2 = solve_cryptarithmetic(problem2_words, problem2_result)
    display_solution("Problem 2", problem2_words, problem2_result, solution2)

if __name__ == "__main__":
    main()
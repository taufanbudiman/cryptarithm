"""
Cryptarithmetic puzzle solver
"""

from itertools import permutations


def solve_cryptarithm(puzzle):
    """
    Solve a cryptarithmetic puzzle.

    Args:
        puzzle: String in format "WORD1 + WORD2 = RESULT"

    Returns:
        Dictionary with solution details or None
    """
    try:
        parts = puzzle.replace(" ", "").upper().split("=")
        if len(parts) != 2:
            return None

        left_side = parts[0]
        result = parts[1]

        if "+" in left_side:
            operands = left_side.split("+")
            operation = "+"
        elif "-" in left_side:
            operands = left_side.split("-")
            operation = "-"
        else:
            return None

        all_words = operands + [result]
        letters = set(''.join(all_words))

        if len(letters) > 10:
            return None

        # Only consider letters as leading if the word has more than 1 character
        # Single character words (like "K" or "D") can be any digit including 0
        leading_letters = set(word[0] for word in all_words if len(word) > 1)

        for perm in permutations(range(10), len(letters)):
            mapping = dict(zip(letters, perm))

            if any(mapping[letter] == 0 for letter in leading_letters):
                continue

            numbers = []
            for word in operands:
                num = int(''.join(str(mapping[c]) for c in word))
                numbers.append(num)

            result_num = int(''.join(str(mapping[c]) for c in result))

            if operation == "+":
                if sum(numbers) == result_num:
                    return {
                        'mapping': mapping,
                        'operands': operands,
                        'result': result,
                        'operation': operation,
                        'numbers': numbers,
                        'result_num': result_num
                    }
            elif operation == "-":
                if numbers[0] - numbers[1] == result_num:
                    return {
                        'mapping': mapping,
                        'operands': operands,
                        'result': result,
                        'operation': operation,
                        'numbers': numbers,
                        'result_num': result_num
                    }

        return None
    except Exception:
        return None
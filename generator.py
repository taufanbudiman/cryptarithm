"""
Cryptarithmetic puzzle generator
"""

import random
import json
from solver import solve_cryptarithm


def generate_3_letter_puzzles(db, target_count=500):
    """
    Generate cryptarithmetic puzzles with only 3 unique letters

    Args:
        db: PuzzleDatabase instance
        target_count: Number of puzzles to generate

    Returns:
        Total puzzle count in database
    """
    current_count = db.get_puzzle_count()
    if current_count >= target_count:
        return current_count

    puzzles_to_generate = target_count - current_count
    attempts = 0
    max_attempts = puzzles_to_generate * 100

    # Use all letters A-Z
    all_letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    # Generate different pattern templates
    # Rule: At least 2 words must have 2+ characters (no pure single letter puzzles like A+B=C)
    patterns = [
        # Pattern: AA + BB = CC (all multi-char)
        lambda a, b, c: f"{a}{a} + {b}{b} = {c}{c}",
        # Pattern: AB + BA = CC (all multi-char)
        lambda a, b, c: f"{a}{b} + {b}{a} = {c}{c}",
        # Pattern: AA + BB = ABC (all multi-char)
        lambda a, b, c: f"{a}{a} + {b}{b} = {a}{b}{c}",
        # Pattern: ABC + ABC = BCA (all multi-char)
        lambda a, b, c: f"{a}{b}{c} + {a}{b}{c} = {b}{c}{a}",
        # Pattern: AB + BA = AC (all multi-char)
        lambda a, b, c: f"{a}{b} + {b}{a} = {a}{c}",
        # Pattern: AAA + BBB = CCC (all multi-char)
        lambda a, b, c: f"{a}{a}{a} + {b}{b}{b} = {c}{c}{c}",
        # Pattern: AB + AB = BAA (all multi-char)
        lambda a, b, c: f"{a}{b} + {a}{b} = {b}{a}{a}",
        # Pattern: ABC + CBA = CAB (all multi-char)
        lambda a, b, c: f"{a}{b}{c} + {c}{b}{a} = {c}{a}{b}",
        # Pattern: AB + BC = CA (all multi-char)
        lambda a, b, c: f"{a}{b} + {b}{c} = {c}{a}",
        # Pattern: ABC + ABC = ABCC (all multi-char)
        lambda a, b, c: f"{a}{b}{c} + {a}{b}{c} = {a}{b}{c}{c}",
        # Pattern: AAB + BAA = BBA (all multi-char)
        lambda a, b, c: f"{a}{a}{b} + {b}{a}{a} = {b}{b}{a}",
        # Pattern: ABA + BAB = CAC (all multi-char)
        lambda a, b, c: f"{a}{b}{a} + {b}{a}{b} = {c}{a}{c}",
        # Pattern: AA + AB = BA (all multi-char)
        lambda a, b, c: f"{a}{a} + {a}{b} = {b}{a}",
        # Pattern: ABC + AB = CAB (all multi-char)
        lambda a, b, c: f"{a}{b}{c} + {a}{b} = {c}{a}{b}",
        # Pattern: AA + B = CC (2 multi-char, 1 single OK)
        lambda a, b, c: f"{a}{a} + {b} = {c}{c}",
        # Pattern: AB + C = BA (2 multi-char, 1 single OK)
        lambda a, b, c: f"{a}{b} + {c} = {b}{a}",
        # Pattern: AAA + B = CCC (2 multi-char, 1 single OK)
        lambda a, b, c: f"{a}{a}{a} + {b} = {c}{c}{c}",
        # Pattern: AB + AB = CC (all multi-char)
        lambda a, b, c: f"{a}{b} + {a}{b} = {c}{c}",
        # Pattern: AA + AA = BB (all multi-char)
        lambda a, b, c: f"{a}{a} + {a}{a} = {b}{b}",
        # Pattern: AAB + C = BAA (2 multi-char, 1 single OK)
        lambda a, b, c: f"{a}{a}{b} + {c} = {b}{a}{a}",
    ]

    # Collect valid puzzles in batches
    batch_size = 50
    puzzle_batch = []

    print(f"Generating {puzzles_to_generate} new puzzles...")

    while len(puzzle_batch) < puzzles_to_generate and attempts < max_attempts:
        attempts += 1

        # Randomly select 3 unique letters from A-Z
        selected_letters = random.sample(all_letters, 3)
        a, b, c = selected_letters

        # Try a random pattern
        pattern = random.choice(patterns)
        puzzle = pattern(a, b, c)

        # Validate: at least 2 words must have 2+ characters
        parts = puzzle.replace(" ", "").split("=")
        left_side = parts[0]
        if "+" in left_side:
            words = left_side.split("+") + [parts[1]]
        elif "-" in left_side:
            words = left_side.split("-") + [parts[1]]
        else:
            continue

        # Count words with 2+ characters
        multi_char_count = sum(1 for word in words if len(word) >= 2)

        # Skip if less than 2 words have multiple characters
        if multi_char_count < 2:
            continue

        # Try to solve it
        solution = solve_cryptarithm(puzzle)

        if solution:
            # Determine difficulty based on complexity
            letter_set = set(puzzle.replace('+', '').replace('=', '').replace(' ', ''))
            puzzle_length = len(
                puzzle.replace('+', '').replace('=', '').replace(' ', ''))

            if puzzle_length <= 8:
                difficulty = "Easy"
            elif puzzle_length <= 12:
                difficulty = "Medium"
            else:
                difficulty = "Hard"

            # Add to batch
            puzzle_batch.append((
                puzzle,
                difficulty,
                len(letter_set),
                json.dumps(solution['mapping'])
            ))

            # Save batch when it reaches batch_size
            if len(puzzle_batch) >= batch_size:
                added = db.add_puzzles_batch(puzzle_batch)
                print(f"Added {added} puzzles... (Total: {db.get_puzzle_count()})")
                puzzle_batch = []

    # Save remaining puzzles
    if puzzle_batch:
        added = db.add_puzzles_batch(puzzle_batch)
        print(f"Added {added} puzzles... (Total: {db.get_puzzle_count()})")

    total = db.get_puzzle_count()
    print(f"✓ Generation complete! Database now contains {total} puzzles")
    return total
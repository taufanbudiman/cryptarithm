# Cryptarithmetic Puzzle Solver & Quiz

A web-based application for solving cryptarithmetic puzzles and testing your skills with an interactive quiz.

## 📁 File Structure

```
cryptarithmetic-app/
│
├── main.py              # Application entry point
├── solver.py            # Cryptarithmetic solving algorithm
├── database.py          # SQLite database management
├── generator.py         # Puzzle generation logic
├── quiz_state.py        # Quiz state management
├── ui_solver.py         # Solver page UI components
├── ui_quiz.py           # Quiz page UI components
│
├── puzzles.db          # SQLite database (auto-generated)
└── puzzles.json        # JSON export (optional)
```

## 🚀 Installation

1. Install NiceGUI:
```bash
pip install nicegui
```

2. Run the application:
```bash
python main.py
```

3. Open browser at: `http://localhost:8080`

## 📦 Module Descriptions

### `main.py`
- Application entry point
- Initializes database and quiz state
- Sets up navigation between Solver and Quiz pages
- Auto-generates initial puzzles on first run

### `solver.py`
- Core cryptarithmetic solving algorithm
- Uses permutations to find valid digit assignments
- Validates leading zeros and arithmetic operations
- Returns complete solution with mapping and verification

### `database.py`
- SQLite database management
- Stores puzzles with difficulty levels
- Batch operations for performance
- WAL mode for concurrent access
- Export to JSON functionality

### `generator.py`
- Generates cryptarithmetic puzzles
- Uses 3 unique letters (A-Z)
- 20+ puzzle patterns
- Ensures at least 2 multi-character words
- Batch generation for efficiency

### `quiz_state.py`
- Manages quiz state (score, attempts, progress)
- Tracks 10-question limit
- Handles hint usage
- Provides quiz completion detection

### `ui_solver.py`
- Solver page interface
- Input field with examples
- Real-time solving
- Visual solution display with mappings

### `ui_quiz.py`
- Quiz page interface
- 10-question quiz system
- Scoring with bonuses
- Hint system
- Final score screen with performance evaluation

## 🎮 Features

### Solver Mode
- Solve any cryptarithmetic puzzle
- Support for addition and subtraction
- Example puzzles included
- Visual solution display

### Quiz Mode
- 10 random questions per quiz
- 3 unique letters per puzzle
- Scoring system:
  - +10 points for correct answer
  - +5 bonus for no hints used
- Hint system (reveals one letter)
- Performance evaluation
- Progress tracking

### Database
- 500+ generated puzzles
- Fast random selection
- Difficulty levels (Easy/Medium/Hard)
- Export to JSON

## 🔧 Configuration

### Puzzle Generation Rules
- Minimum 2 words with 2+ characters
- 3 unique letters (A-Z)
- No pure single-letter puzzles (e.g., A + B = C)
- Valid patterns: AA + BB = CC, KK + Z = SS, etc.

### Quiz Settings
- Questions per quiz: 10 (configurable in `quiz_state.py`)
- Points per correct answer: 10
- No-hint bonus: 5
- Letter count: 3

## 🐛 Bug Fixes Applied

1. ✅ Fixed hint button functionality
2. ✅ Changed from ABC-only to full A-Z alphabet
3. ✅ Accepts any mathematically valid solution
4. ✅ Prevents single-letter arbitrary puzzles
5. ✅ Fixed multiple scoring on same question
6. ✅ Fixed database locking issues

## 📝 Example Puzzles

### Easy
- AA + BB = CC
- AB + BA = CC
- KK + Z = SS

### Medium
- ABC + ABC = BCA
- AAB + BAA = BBA

### Hard
- ABC + ABC = ABCC
- AAA + BBB = CCC

## 🎯 Usage Tips

1. Start with Solver mode to understand the puzzles
2. Try example puzzles first
3. Use hints sparingly in Quiz mode for bonus points
4. Generate more puzzles if needed
5. Export puzzles to JSON for backup

## 🔐 Technical Details

- **Framework**: NiceGUI (Python web framework)
- **Database**: SQLite with WAL mode
- **Algorithm**: Brute-force permutation search
- **UI**: Tailwind CSS classes
- **Storage**: Persistent SQLite database

## 📊 Performance

- Puzzle generation: ~500 puzzles in seconds
- Solving speed: Near-instant for 3-letter puzzles
- Database queries: Optimized with batch operations
- No backend API required - all runs locally

## 🤝 Contributing

Feel free to extend the application:
- Add subtraction puzzles
- Increase letter count
- Add difficulty modes
- Implement leaderboards
- Add timer challenges

## 📄 License

Free to use and modify for educational purposes.

---

**Enjoy solving cryptarithmetic puzzles! 🧩**

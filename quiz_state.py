"""
Quiz state management
"""


class QuizState:
    """Manage quiz state and scoring"""

    def __init__(self, db):
        self.db = db
        self.current_puzzle = None
        self.score = 0
        self.attempts = 0
        self.hints_used = 0
        self.questions_answered = 0
        self.max_questions = 10

    def new_puzzle(self):
        """Get a new random puzzle"""
        self.current_puzzle = self.db.get_random_puzzle(letter_count=3)
        self.hints_used = 0
        return self.current_puzzle

    def is_quiz_complete(self):
        """Check if quiz is complete"""
        return self.questions_answered >= self.max_questions

    def reset(self):
        """Reset quiz state"""
        self.score = 0
        self.attempts = 0
        self.hints_used = 0
        self.questions_answered = 0
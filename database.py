"""
SQLite database management for puzzles
"""

import sqlite3
import json


class PuzzleDatabase:
    """Manage puzzle database with SQLite"""

    def __init__(self, db_path='puzzles.db'):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """Get a database connection with timeout"""
        conn = sqlite3.connect(self.db_path, timeout=30.0, check_same_thread=False)
        conn.execute(
            'PRAGMA journal_mode=WAL')  # Enable WAL mode for better concurrency
        return conn

    def init_database(self):
        """Initialize database schema"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS puzzles
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               puzzle
                               TEXT
                               UNIQUE
                               NOT
                               NULL,
                               difficulty
                               TEXT
                               NOT
                               NULL,
                               letter_count
                               INTEGER
                               NOT
                               NULL,
                               solution
                               TEXT
                               NOT
                               NULL,
                               created_at
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP
                           )
                           ''')
            conn.commit()
        finally:
            conn.close()

    def add_puzzle(self, puzzle, difficulty, letter_count, solution):
        """Add a puzzle to database"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO puzzles (puzzle, difficulty, letter_count, solution)
                           VALUES (?, ?, ?, ?)
                           ''',
                           (puzzle, difficulty, letter_count, json.dumps(solution)))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def add_puzzles_batch(self, puzzles_list):
        """Add multiple puzzles in a batch for better performance"""
        conn = self.get_connection()
        added = 0
        try:
            cursor = conn.cursor()
            for puzzle_data in puzzles_list:
                try:
                    cursor.execute('''
                                   INSERT INTO puzzles (puzzle, difficulty, letter_count, solution)
                                   VALUES (?, ?, ?, ?)
                                   ''', puzzle_data)
                    added += 1
                except sqlite3.IntegrityError:
                    pass  # Skip duplicates
            conn.commit()
        finally:
            conn.close()
        return added

    def get_puzzle_count(self):
        """Get total puzzle count"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM puzzles')
            count = cursor.fetchone()[0]
            return count
        finally:
            conn.close()

    def get_random_puzzle(self, letter_count=3):
        """Get a random puzzle"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                           SELECT puzzle, difficulty, solution
                           FROM puzzles
                           WHERE letter_count = ?
                           ORDER BY RANDOM() LIMIT 1
                           ''', (letter_count,))

            result = cursor.fetchone()

            if result:
                return {
                    'puzzle': result[0],
                    'difficulty': result[1],
                    'solution': json.loads(result[2])
                }
            return None
        finally:
            conn.close()

    def get_all_puzzles(self, letter_count=None):
        """Get all puzzles, optionally filtered by letter count"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()

            if letter_count:
                cursor.execute('''
                               SELECT puzzle, difficulty, solution
                               FROM puzzles
                               WHERE letter_count = ?
                               ''', (letter_count,))
            else:
                cursor.execute('SELECT puzzle, difficulty, solution FROM puzzles')

            results = cursor.fetchall()

            return [{
                'puzzle': r[0],
                'difficulty': r[1],
                'solution': json.loads(r[2])
            } for r in results]
        finally:
            conn.close()

    def clear_database(self):
        """Clear all puzzles"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM puzzles')
            conn.commit()
        finally:
            conn.close()

    def export_to_json(self, filename='puzzles.json'):
        """Export puzzles to JSON file"""
        puzzles = self.get_all_puzzles()
        with open(filename, 'w') as f:
            json.dump(puzzles, f, indent=2)
        return len(puzzles)
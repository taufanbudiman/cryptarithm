"""
SQLite and MongoDB database management for puzzles
"""

import sqlite3
import json
import os
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class PuzzleDatabase:
    """Manage puzzle database with SQLite or MongoDB"""

    def __init__(self, connection_string=None):
        """
        Initialize database connection.

        Args:
            connection_string: Either MongoDB URI (e.g., "mongodb://localhost:27017/cryptarithm")
                             or SQLite file path (e.g., "/tmp/puzzles.db").
                             If not provided, checks MONGODB_URI env var, then DB_PATH env var,
                             then defaults to "/tmp/puzzles.db" for SQLite.
        """
        # Determine connection string from argument or environment
        conn_str = connection_string or os.environ.get('MONGODB_URI') or os.environ.get('DB_PATH', '/tmp/puzzles.db')

        # Detect if it's a MongoDB URI
        if conn_str.startswith(('mongodb://', 'mongodb+srv://')):
            # Use MongoDB
            self.client = MongoClient(conn_str)
            db_name = conn_str.split('/')[-1] if '/' in conn_str else 'cryptarithm'
            self.db = self.client[db_name]
            self.collection = self.db['puzzles']
            self._use_mongo = True
            self._init_mongo_indexes()
        else:
            # Use SQLite
            self.db_path = conn_str
            self._use_mongo = False
            self.init_database()

    def _init_mongo_indexes(self):
        """Initialize MongoDB indexes"""
        self.collection.create_index([('puzzle', 1)], unique=True)
        self.collection.create_index([('letter_count', 1)])

    def get_connection(self):
        """Get a database connection with timeout (SQLite only)"""
        if self._use_mongo:
            raise NotImplementedError("Use self.collection for MongoDB operations")
        conn = sqlite3.connect(self.db_path, timeout=30.0, check_same_thread=False)
        conn.execute(
            'PRAGMA journal_mode=WAL')  # Enable WAL mode for better concurrency
        return conn

    def init_database(self):
        """Initialize database schema (SQLite only)"""
        if self._use_mongo:
            return  # MongoDB uses schema-less design
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
        if self._use_mongo:
            try:
                self.collection.insert_one({
                    'puzzle': puzzle,
                    'difficulty': difficulty,
                    'letter_count': letter_count,
                    'solution': solution
                })
                return True
            except DuplicateKeyError:
                return False
        else:
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
        if self._use_mongo:
            added = 0
            for puzzle_data in puzzles_list:
                try:
                    self.collection.insert_one({
                        'puzzle': puzzle_data[0],
                        'difficulty': puzzle_data[1],
                        'letter_count': puzzle_data[2],
                        'solution': puzzle_data[3]
                    })
                    added += 1
                except DuplicateKeyError:
                    pass
            return added
        else:
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
        if self._use_mongo:
            return self.collection.count_documents({})
        else:
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
        if self._use_mongo:
            result = self.collection.aggregate([
                {'$match': {'letter_count': letter_count}},
                {'$sample': {'size': 1}}
            ])
            doc = next(result, None)
            if doc:
                return {
                    'puzzle': doc['puzzle'],
                    'difficulty': doc['difficulty'],
                    'solution': doc['solution']
                }
            return None
        else:
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
        if self._use_mongo:
            query = {'letter_count': letter_count} if letter_count else {}
            results = self.collection.find(query)
            return [{
                'puzzle': r['puzzle'],
                'difficulty': r['difficulty'],
                'solution': r['solution']
            } for r in results]
        else:
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
        if self._use_mongo:
            self.collection.delete_many({})
        else:
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

    def close(self):
        """Close database connection"""
        if self._use_mongo:
            self.client.close()
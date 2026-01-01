"""
Quiz page UI components
Note: This is a large file, split into logical sections
"""

from nicegui import ui
import random
from solver import solve_cryptarithm
from generator import generate_3_letter_puzzles
from ui_solver import display_solution


def show_final_score(quiz_state, quiz_container, start_quiz_func, reset_quiz_func):
    """Show final score screen"""
    quiz_container.clear()

    with quiz_container:
        with ui.card().classes(
                'w-full p-8 bg-gradient-to-r from-yellow-400 to-orange-500'):
            ui.label('🎉 Quiz Complete!').classes('text-4xl font-bold text-white mb-4')
            ui.label(f'Final Score: {quiz_state.score}').classes(
                'text-3xl font-bold text-white mb-2')
            ui.label(f'Questions Answered: {quiz_state.questions_answered}').classes(
                'text-xl text-white mb-2')
            ui.label(f'Total Attempts: {quiz_state.attempts}').classes(
                'text-xl text-white')

        # Performance evaluation
        with ui.card().classes('w-full p-6 mt-6'):
            ui.label('📊 Performance').classes('text-2xl font-bold text-gray-800 mb-4')

            avg_score = quiz_state.score / quiz_state.questions_answered if quiz_state.questions_answered > 0 else 0

            if avg_score >= 14:
                performance = "🌟 Excellent! Perfect score!"
                color = "text-green-600"
            elif avg_score >= 12:
                performance = "👏 Great job! Very good!"
                color = "text-blue-600"
            elif avg_score >= 10:
                performance = "👍 Good work! Keep practicing!"
                color = "text-indigo-600"
            else:
                performance = "💪 Keep practicing! You can do better!"
                color = "text-orange-600"

            ui.label(performance).classes(f'text-xl font-semibold {color}')
            ui.label(f'Average score per question: {avg_score:.1f}').classes(
                'text-lg text-gray-600 mt-2')

        # Action buttons
        with ui.row().classes('gap-4 mt-6 justify-center'):
            ui.button('🔄 Start New Quiz', on_click=reset_quiz_func).classes(
                'bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-xl px-8 py-4'
            )


def create_quiz_question(quiz_container, quiz_state, solution, puzzle, difficulty,
                         update_score_func, start_quiz_func, show_final_score_func):
    """Create a single quiz question UI"""

    with quiz_container:
        with ui.card().classes('w-full p-6'):
            with ui.row().classes('w-full justify-between items-center mb-4'):
                ui.label(f'Puzzle: {puzzle}').classes(
                    'text-2xl font-bold text-gray-800')
                ui.badge(difficulty, color='primary').classes('text-lg px-4 py-2')

            ui.label('Enter the digit for each letter:').classes(
                'text-lg text-gray-600 mb-4')

            # Get unique letters
            letters = sorted(
                set(puzzle.replace('+', '').replace('=', '').replace(' ', '')))

            # Create input fields
            inputs = {}
            with ui.grid(columns='auto auto auto').classes('gap-4 mb-4'):
                for letter in letters:
                    with ui.column().classes('items-center'):
                        ui.label(letter).classes('text-2xl font-bold text-purple-600')
                        inputs[letter] = ui.number(
                            min=0, max=9,
                            placeholder='0-9'
                        ).classes('w-20 text-center text-xl')

            answer_container = ui.column().classes('w-full mt-4')
            question_answered = False  # Track if this question has been answered correctly

            def check_answer():
                nonlocal question_answered

                # Prevent scoring multiple times for the same question
                if question_answered:
                    ui.notify('Already answered! Click Next Question.', type='warning')
                    return

                quiz_state.attempts += 1
                update_score_func()

                user_mapping = {}
                for letter, input_field in inputs.items():
                    if input_field.value is None:
                        with answer_container:
                            answer_container.clear()
                            ui.notify('Please fill all letters!', type='warning')
                            ui.label('⚠️ Please enter a digit for each letter').classes(
                                'text-xl text-orange-600')
                        return
                    user_mapping[letter] = int(input_field.value)

                # Check if all digits are unique
                if len(set(user_mapping.values())) != len(user_mapping):
                    with answer_container:
                        answer_container.clear()
                        ui.notify('Digits must be unique!', type='warning')
                        ui.label('⚠️ Each letter must have a different digit').classes(
                            'text-xl text-orange-600')
                    return

                # Verify the answer by recalculating
                try:
                    # Convert words to numbers using user's mapping
                    user_operands = []
                    for word in solution['operands']:
                        num_str = ''.join(str(user_mapping[c]) for c in word)
                        user_operands.append(int(num_str))

                    user_result = ''.join(
                        str(user_mapping[c]) for c in solution['result'])
                    user_result_num = int(user_result)

                    # Check if the equation is valid
                    if solution['operation'] == '+':
                        calculated = sum(user_operands)
                    else:
                        calculated = user_operands[0] - user_operands[1]

                    is_correct = (calculated == user_result_num)
                except:
                    is_correct = False

                # Check if solution is correct
                if is_correct:
                    question_answered = True  # Mark question as answered
                    quiz_state.score += 10
                    if quiz_state.hints_used == 0:
                        quiz_state.score += 5  # Bonus for no hints
                    quiz_state.questions_answered += 1
                    update_score_func()

                    # Disable all inputs after correct answer
                    for input_field in inputs.values():
                        input_field.set_enabled(False)

                    with answer_container:
                        answer_container.clear()
                        with ui.card().classes(
                                'w-full bg-green-50 border-2 border-green-400 p-6'):
                            ui.label('🎉 Correct!').classes(
                                'text-3xl font-bold text-green-700')
                            ui.label(
                                f'+{10 + (5 if quiz_state.hints_used == 0 else 0)} points').classes(
                                'text-xl text-green-600')

                            if quiz_state.is_quiz_complete():
                                ui.label(
                                    f'Quiz Complete! ({quiz_state.questions_answered}/{quiz_state.max_questions})').classes(
                                    'text-lg text-green-600 mt-2')
                                ui.button('📊 View Results',
                                          on_click=show_final_score_func).classes(
                                    'mt-4 bg-yellow-500 text-white text-lg px-6 py-3'
                                )
                            else:
                                ui.label(
                                    f'Progress: {quiz_state.questions_answered}/{quiz_state.max_questions}').classes(
                                    'text-lg text-green-600 mt-2')
                                ui.button('Next Question →',
                                          on_click=start_quiz_func).classes(
                                    'mt-4 bg-green-600 text-white text-lg px-6 py-3'
                                )
                    ui.notify('Correct! 🎉', type='positive')
                else:
                    with answer_container:
                        answer_container.clear()
                        with ui.card().classes(
                                'w-full bg-red-50 border-2 border-red-400 p-6'):
                            ui.label('❌ Incorrect!').classes(
                                'text-2xl font-bold text-red-700')
                            ui.label('Try again or use a hint').classes('text-red-600')
                    ui.notify('Incorrect, try again!', type='negative')

            def show_hint():
                quiz_state.hints_used += 1
                # Show one random correct mapping
                available_letters = [l for l in inputs.keys() if inputs[l].enabled]
                if available_letters:
                    random_letter = random.choice(available_letters)
                    correct_digit = solution['mapping'][random_letter]
                    inputs[random_letter].value = correct_digit
                    inputs[random_letter].set_enabled(False)
                    ui.notify(f'Hint: {random_letter} = {correct_digit}', type='info')
                else:
                    ui.notify('All hints already shown!', type='warning')

            def show_solution():
                quiz_state.questions_answered += 1
                update_score_func()
                answer_container.clear()

                with answer_container:
                    ui.label('💡 Solution Shown (No points awarded)').classes(
                        'text-xl text-orange-600 mb-4')

                display_solution(answer_container, puzzle, solution)

                with answer_container:
                    if quiz_state.is_quiz_complete():
                        ui.label(
                            f'Quiz Complete! ({quiz_state.questions_answered}/{quiz_state.max_questions})').classes(
                            'text-lg text-gray-600 mt-2')
                        ui.button('📊 View Results',
                                  on_click=show_final_score_func).classes(
                            'mt-4 bg-yellow-500 text-white text-lg px-6 py-3'
                        )
                    else:
                        ui.label(
                            f'Progress: {quiz_state.questions_answered}/{quiz_state.max_questions}').classes(
                            'text-lg text-gray-600 mt-2')
                        ui.button('Next Question →', on_click=start_quiz_func).classes(
                            'mt-4 bg-indigo-600 text-white text-lg px-6 py-3'
                        )

            with ui.row().classes('gap-4 mt-4'):
                ui.button('✓ Check Answer', on_click=check_answer).classes(
                    'bg-gradient-to-r from-green-500 to-green-600 text-white text-lg px-6 py-3'
                )
                ui.button('💡 Hint', on_click=show_hint).classes(
                    'bg-yellow-500 text-white text-lg px-6 py-3'
                )
                ui.button('👁 Show Solution', on_click=show_solution).classes(
                    'bg-gray-500 text-white text-lg px-6 py-3'
                )


def create_quiz_page(content_area, db, quiz_state):
    """Create the quiz interface - Main entry point"""
    content_area.clear()

    with content_area:
        ui.label('🎯 Cryptarithmetic Quiz').classes(
            'text-4xl font-bold text-indigo-700 mb-2')
        ui.label('Test your puzzle-solving skills! (10 questions per quiz)').classes(
            'text-gray-600 mb-4')

        # Database info
        puzzle_count = db.get_puzzle_count()
        db_info = ui.label(f'📚 Database: {puzzle_count} puzzles available').classes(
            'text-lg text-gray-700 mb-6')

        # Score display
        score_card = ui.card().classes(
            'w-full p-6 bg-gradient-to-r from-indigo-500 to-purple-600')

        with score_card:
            with ui.row().classes('w-full justify-between items-center'):
                score_label = ui.label(f'Score: {quiz_state.score}').classes(
                    'text-3xl font-bold text-white')
                with ui.column().classes('items-end'):
                    attempts_label = ui.label(
                        f'Attempts: {quiz_state.attempts}').classes(
                        'text-xl text-white')
                    question_label = ui.label(
                        f'Question: {quiz_state.questions_answered}/{quiz_state.max_questions}').classes(
                        'text-xl text-white')

        # Quiz area
        quiz_container = ui.column().classes('w-full mt-6')

        def update_score():
            score_label.text = f'Score: {quiz_state.score}'
            attempts_label.text = f'Attempts: {quiz_state.attempts}'
            question_label.text = f'Question: {quiz_state.questions_answered}/{quiz_state.max_questions}'

        def show_final_score_wrapper():
            show_final_score(quiz_state, quiz_container, start_quiz, reset_quiz)

        def start_quiz():
            if quiz_state.is_quiz_complete():
                show_final_score_wrapper()
                return

            quiz_container.clear()
            puzzle_data = quiz_state.new_puzzle()

            if not puzzle_data:
                with quiz_container:
                    ui.label('No puzzles available! Generate puzzles first.').classes(
                        'text-xl text-red-600')
                return

            puzzle = puzzle_data['puzzle']
            difficulty = puzzle_data['difficulty']
            solution = solve_cryptarithm(puzzle)

            create_quiz_question(
                quiz_container, quiz_state, solution, puzzle, difficulty,
                update_score, start_quiz, show_final_score_wrapper
            )

        def reset_quiz():
            quiz_state.reset()
            update_score()
            start_quiz()

        def generate_puzzles():
            ui.notify('Generating puzzles... Please wait', type='info')
            count = generate_3_letter_puzzles(db, 500)
            db_info.text = f'📚 Database: {count} puzzles available'
            ui.notify(f'Generated! Total: {count} puzzles', type='positive')

        def export_puzzles():
            count = db.export_to_json('puzzles.json')
            ui.notify(f'Exported {count} puzzles to puzzles.json', type='positive')

        # Start/Reset buttons
        with ui.row().classes('gap-4 mt-6'):
            ui.button('🎮 Start Quiz', on_click=start_quiz).classes(
                'bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-xl px-8 py-4'
            )
            ui.button('🔄 Reset Score', on_click=reset_quiz).classes(
                'bg-gray-400 text-white text-xl px-8 py-4'
            )

        # Database management
        with ui.card().classes('w-full p-6 mt-6 bg-gray-50'):
            ui.label('🗄️ Database Management').classes('text-xl font-semibold mb-4')
            with ui.row().classes('gap-4'):
                ui.button('➕ Generate 500 Puzzles', on_click=generate_puzzles).classes(
                    'bg-blue-600 text-white px-6 py-3'
                )
                ui.button('📥 Export to JSON', on_click=export_puzzles).classes(
                    'bg-green-600 text-white px-6 py-3'
                )
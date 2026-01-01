from nicegui import ui
from database import PuzzleDatabase
from quiz_state import QuizState
from generator import generate_3_letter_puzzles
from ui_solver import create_solver_page
from ui_quiz import create_quiz_page

# Initialize global instances
db = PuzzleDatabase()
quiz_state = QuizState(db)


@ui.page('/')
def main_page():
    """Main application page with navigation"""
    ui.colors(primary='#667eea')

    with ui.header().classes(
            'items-center justify-between bg-gradient-to-r from-purple-600 to-indigo-600'):
        ui.label('🔢 Cryptarithmetic App').classes('text-2xl font-bold text-white')

        with ui.row().classes('gap-2'):
            solver_btn = ui.button('📊 Solver',
                                   on_click=lambda: show_page('solver')).classes(
                'bg-white text-purple-700 font-semibold'
            )
            quiz_btn = ui.button('🎯 Quiz', on_click=lambda: show_page('quiz')).classes(
                'bg-purple-500 text-white font-semibold'
            )

    # Main content area
    content_area = ui.column().classes('w-full max-w-5xl mx-auto p-8')

    def show_page(page_name):
        """Switch between pages"""
        if page_name == 'solver':
            solver_btn.classes('bg-white text-purple-700 font-semibold',
                               remove='bg-purple-500 text-white')
            quiz_btn.classes('bg-purple-500 text-white font-semibold',
                             remove='bg-white text-purple-700')
            create_solver_page(content_area)
        elif page_name == 'quiz':
            quiz_btn.classes('bg-white text-indigo-700 font-semibold',
                             remove='bg-purple-500 text-white')
            solver_btn.classes('bg-purple-500 text-white font-semibold',
                               remove='bg-white text-purple-700')
            create_quiz_page(content_area, db, quiz_state)

    # Show solver page by default
    show_page('solver')


if __name__ in {"__main__", "__mp_main__"}:
    # Generate initial puzzles if database is empty
    if db.get_puzzle_count() == 0:
        print("Generating initial puzzle database...")
        generate_3_letter_puzzles(db, 500)

    ui.run(
        title='Cryptarithmetic App',
        favicon='🔢',
        dark=False,
        reload=True,
        show=True,
        port=8080
    )
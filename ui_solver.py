"""
Solver page UI components
"""

from nicegui import ui
from solver import solve_cryptarithm


def display_solution(container, puzzle, solution):
    """Display the solution in a nice format"""
    mapping = solution['mapping']
    numbers = solution['numbers']
    result_num = solution['result_num']
    operation = solution['operation']

    with container:
        with ui.card().classes('w-full bg-gradient-to-r from-purple-500 to-indigo-600'):
            ui.label('✅ Solution Found!').classes('text-3xl font-bold text-white')
            ui.label(puzzle).classes('text-xl text-white mt-2')

        ui.separator()

        ui.label('Letter to Digit Mapping:').classes(
            'text-2xl font-bold text-purple-700 mt-4')

        with ui.grid(columns='auto auto auto auto auto').classes('gap-4 mt-4'):
            for letter in sorted(mapping.keys()):
                with ui.card().classes(
                        'bg-gray-50 border-2 border-gray-300 p-4 text-center'):
                    ui.label(letter).classes('text-3xl font-bold text-purple-600')
                    ui.label('↓').classes('text-lg text-gray-500')
                    ui.label(str(mapping[letter])).classes(
                        'text-4xl font-bold text-gray-800')

        ui.separator().classes('my-6')

        with ui.card().classes('w-full bg-green-50 border-2 border-green-400'):
            ui.label('🎯 Verification:').classes('text-2xl font-bold text-green-700')

            op_symbol = '+' if operation == '+' else '−'
            equation = f"{' {} '.format(op_symbol).join(map(str, numbers))} = {result_num}"
            ui.label(equation).classes('text-2xl font-bold text-gray-800 mt-2')

            calc_result = sum(numbers) if operation == '+' else numbers[0] - numbers[1]
            ui.label(f'{calc_result} = {result_num} ✓').classes(
                'text-2xl font-bold text-green-600 mt-2')


def create_solver_page(content_area):
    """Create the solver interface"""
    content_area.clear()

    with content_area:
        ui.label('🔢 Cryptarithmetic Puzzle Solver').classes(
            'text-4xl font-bold text-purple-700 mb-2')
        ui.label(
            'Each letter represents a unique digit (0-9). Leading letters cannot be zero.').classes(
            'text-gray-600 mb-6'
        )

        # Input section
        with ui.card().classes('w-full p-6'):
            ui.label('Enter your puzzle:').classes('text-xl font-semibold mb-2')
            puzzle_input = ui.input(
                placeholder='e.g., SEND + MORE = MONEY'
            ).classes('w-full text-lg')

            result_container = ui.column().classes('w-full mt-4')

            def solve_puzzle():
                result_container.clear()
                puzzle = puzzle_input.value.strip()

                if not puzzle:
                    with result_container:
                        ui.notify('Please enter a puzzle!', type='warning')
                        ui.label('⚠️ Please enter a puzzle to solve').classes(
                            'text-xl text-orange-600')
                    return

                with result_container:
                    ui.label('🔍 Solving puzzle...').classes('text-lg text-blue-600')

                solution = solve_cryptarithm(puzzle)
                result_container.clear()

                if solution:
                    display_solution(result_container, puzzle, solution)
                    ui.notify('Solution found!', type='positive')
                else:
                    with result_container:
                        with ui.card().classes(
                                'w-full bg-red-50 border-2 border-red-400'):
                            ui.label('❌ No Solution Found').classes(
                                'text-2xl font-bold text-red-700')
                            ui.label('This puzzle has no valid solution.').classes(
                                'text-red-600')

            def clear_all():
                puzzle_input.value = ''
                result_container.clear()
                ui.notify('Cleared!', type='info')

            def load_example(example):
                puzzle_input.value = example
                solve_puzzle()

            puzzle_input.on('keydown.enter', solve_puzzle)

            # Buttons
            with ui.row().classes('w-full gap-4 mt-4'):
                ui.button('🚀 Solve Puzzle', on_click=solve_puzzle).classes(
                    'flex-1 bg-gradient-to-r from-purple-500 to-indigo-600 text-white text-lg py-3'
                )
                ui.button('🔄 Clear', on_click=clear_all).classes(
                    'flex-1 bg-gray-300 text-gray-700 text-lg py-3'
                )

        # Examples section
        with ui.card().classes('w-full p-6 mt-6'):
            ui.label('📝 Try These Examples:').classes('text-xl font-semibold mb-4')

            examples = [
                'SEND + MORE = MONEY',
                'TWO + TWO = FOUR',
                'BASE + BALL = GAMES',
                'EAT + THAT = APPLE'
            ]

            with ui.row().classes('gap-2 flex-wrap'):
                for example in examples:
                    ui.button(
                        example,
                        on_click=lambda e=example: load_example(e)
                    ).classes('bg-gray-100 text-gray-700 hover:bg-purple-100')
# python-sudoku-solver
A python script that solves any valid sudoku puzzle.

Author:
Bas Donker

Dependancies:
  - Must have Python 3.x installed.
  - Must have an unsolved sudoku puzzle in a .txt file.

Usage:
- Either use the sample file "sudoku.txt" or create a new sudoku puzzle in the following format in a .txt file:
  - 9 lines for the 9 rows in a sudoku puzzle
  - 9 characters on every line
  - Use a dot (".") to indicate an empty cell
  - Fill in every clue in the correct row and columns
  - You can add characters like "|", "-", and "+" for readability purposes, but this is optional
- Run the solver with the following command:
  sudoku_solver.py <file location of unsolved puzzle>
  example:
  sudoku_solver.py sudoku_puzzle.txt
- Allow for some time for the solver to finish
- Once the solver has completed, the solution is saved in a new file in the same location as the original puzzle with the following name:
  <original file name>_SOLVED.txt
  example:
  sudoku_puzzle_SOLVED.txt

Errors:
- ERROR 600: Incorrect number of digits. Got: <x>, expected: 81
    The sudoku puzzle contains an incorrect number of digits. Review the puzzle to correct this
- ERROR 601: Puzzle not valid
    The puzzle is not solvable by the rules of sudoku. The most common cause is a digit being in a row, column or sub-grid more than once.
- ERROR 503: No file specified
    No file was specified in the command to run the solver. Run the solver with the following command:
      sudoku_solver.py <file location of unsolved puzzle>
      example:
      sudoku_solver.py sudoku_puzzle.txt
- ERROR 502: File not found
    The file specified is not available

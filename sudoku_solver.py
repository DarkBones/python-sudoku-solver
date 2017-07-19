import sys
import os.path

# MAIN Function
def start(filename):
  txt = read_file(filename)
  
  if txt == False:
    print("ERROR 502: File not found")
    return
  
  number_array = txt_to_number_array(txt)
  
  if len(number_array) != 81:
    print("ERROR 600: Incorrect number of digits. Got: %s expected: 81" % len(number_array))
    return
  
  grid = array_to_grid(number_array)
  valid_puzzle = validate_puzzle(grid)
  
  if valid_puzzle == False:
    print("ERROR 601: Puzzle not valid")
    return
  
  print_grid(grid)
  steps = solve_grid(grid)
  print_grid(grid)
  
  valid_solution = validate_solution(grid)
  
  if valid_solution == True:
    new_filename = filename.replace(".txt", "_solved.txt")
  else:
    new_filename = filename.replace(".txt", "_FAILED.txt")
  
  save_grid(new_filename, grid)
  
  print("Solution valid: %s" % valid_solution)
  print("Steps taken: %s" % steps)

# Solving the grid
def solve_grid(grid):
  cells = unassigned_cells(grid)
  
  c = 0
  steps = 0
  while c < len(cells):
    steps += 1
    
    x = cells[c][0]
    y = cells[c][1]
    
    n = next_legal(grid, x, y)
    if n > 0:
      grid[y][x] = n
    else:
      while c >= 0:
        c -= 1
        x = cells[c][0]
        y = cells[c][1]
        
        n = next_legal(grid, x, y)
        if n > 0:
          grid[y][x] = n
          break
        else:
          grid[y][x] = 0
    c += 1
  return steps
  
# Checks if this puzzle is solvable
def validate_puzzle(grid):
  # Check the rows
  n = 1
  while n <= 9:
    y = 0
    while y < 9:
      count = 0
      x = 0
      while x < 9:
        if grid[y][x] == n:
          count += 1
          if count > 1:
            print(n, x, y)
            return False
        x += 1
      y += 1
    n += 1
  
  # Check the cols
  n = 1
  while n <= 9:
    x = 0
    while x < 9:
      count = 0
      y = 0
      while y < 9:
        if grid[y][x] == n:
          count += 1
          if count > 1:
            return False
        y += 1
      x += 1
    n += 1
    
  # Check the sub-grids
  n = 1
  while n <= 9:
    y = 0
    while y < 9:
      x = 0
      while x < 9:
        yind = y
        count = 0
        while yind < y + 3:
          xind = x
          while xind < x + 3:
            if grid[yind][xind] == n:
              count += 1
              if count > 1:
                return False
            xind += 1
          yind += 1
        x += 3
      y += 3
    n += 1
    
  return True
  
# Checks if the solution is valid
def validate_solution(grid):
  # Check the rows
  n = 1
  while n <= 9:
    y = 0
    while y < 9:
      if is_in_row(grid, y, n) == False:
        return False
      y += 1
    n += 1
    
  # Check the columns
  n = 1
  while n <= 9:
    x = 0
    while x < 9:
      if is_in_col(grid, x, n) == False:
        return False
      x += 1
    n += 1
    
  # Check the sub-grids
  n = 1
  while n <= 9:
    y = 0
    while y < 9:
      x = 0
      while x < 9:
        if is_in_box(grid, x, y, n) == False:
          return False
        x += 3
      y += 3
    n += 1
  return True
  
# Returns the next legal number for cell. Returns -1 if no legal number is available
def next_legal(grid, x, y):
  n = grid[y][x] + 1
  while n <= 9:
    if number_is_legal(grid, x, y, n) == True:
      return n
    n += 1
  return -1
    
# Saves the current grid to a txt file
def save_grid(filename, grid):
  f = open(filename, "w+")
  y = 0
  while y < 9:
    f.write(str(grid[y][0]) + str(grid[y][1]) + str(grid[y][2]) + "|" + str(grid[y][3]) + str(grid[y][4]) + str(grid[y][5]) + "|" + str(grid[y][6]) + str(grid[y][7]) + str(grid[y][8]))
    if y < 8:
      f.write("\n")
    if(y + 1) % 3 == 0 and y < 8:
      f.write("---+---+---\n")
    y+= 1
  f.close()

# Prints the grid in a readable format
def print_grid(grid):
  y = 0
  print("----------------------")
  while y < 9:
    print(str(grid[y][0]), str(grid[y][1]), str(grid[y][2]), "|", str(grid[y][3]), str(grid[y][4]), str(grid[y][5]), "|", str(grid[y][6]), str(grid[y][7]), str(grid[y][8]))
    if (y + 1) % 3 == 0:
      print("------+-------+-------")
    y += 1
    
# returns an array of unassigned cells for backtracking purposes
def unassigned_cells(grid):
  cells = []
  y = 0
  while y < 9:
    x = 0
    while x < 9:
      if grid[y][x] == 0:
        cells.append((x, y))
      x += 1
    y += 1
  return cells
    
# returns True if a number is legal for a cell
def number_is_legal(grid, x, y, n):
  in_row = is_in_row(grid, y, n)
  in_col = is_in_col(grid, x, n)
  in_box = is_in_box(grid, x, y, n)
  
  if in_row == True or in_col == True or in_box == True:
    return False
  else:
    return True

# Checks if number is present in row
def is_in_row(grid, r, n):
  return n in grid[r]
  
# Checks if number is present in column
def is_in_col(grid, x, n):
  r = 0
  while r < 9:
    if grid[r][x] == n:
      return True
    r += 1
    
  return False
  
# Checks if number is present in sub-grid
def is_in_box(grid, x, y, n):
  # Find the right most 'x' of the sub-grid
  while x % 3 != 0:
    x -= 1
    
  # Find the upper most 'y' of the sub-grid
  while y % 3 != 0:
    y -= 1
    
  # Go through all cells in the sub-grid to see if 'n' is present
  yind = y
  while yind < y + 3:
    xind = x
    while xind < x + 3:
      if grid[yind][xind] == n:
        return True
      xind += 1
    yind += 1
  return False
  
# Reads the txt file containing the unsolved sudoku puzzle
def read_file(filename):
  if os.path.exists(filename):
    f = open(filename)
    return f.readlines()
  else:
    return False

# Takes the read txt file and transforms it into an array of numbers  
def txt_to_number_array(txt):
  number_array = []
  for l in txt:
    l = l.replace(".", "0")
    
    i = 0
    while i < len(l):
      try:
        n = int(l[i])
        number_array.append(n)
      except ValueError:
        n = n
      i += 1
  return number_array
  
# Takes an array of 81 numbers and forms a 9 by 9 grid
def array_to_grid(number_array):
  grid = []
  row = []
  i = 0
  while len(grid) < 9:
    while i < 81:
      row.append(number_array[i])
      i += 1
      
      if i % 9 == 0 and i < 81:
        grid.append(row)
        row = []
    grid.append(row)
  return grid
  
if __name__ == "__main__":
  if len(sys.argv) > 1:
    start(sys.argv[1])
  else:
    print("ERROR 503: No file specified")

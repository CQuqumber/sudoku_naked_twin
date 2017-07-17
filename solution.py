
assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def valid_cols_rows(cols, rows, diag):
    '''Assert statements to check input variables'''
    assert len(cols) == len(rows), "Cols and Rows have different length."
    assert len(diag) == 81, "Sudoku length: %d" % len(diag)



def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]


diagonal_units = [[r+c for r,c in zip(rows,cols)], [r+c for r,c in zip(rows,cols[::-1])]]

diagonal = True  ## From forum mentor

if diagonal:
    unitlist = row_units + column_units + square_units + diagonal_units
else:
    unitlist = row_units + column_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    ##  Find all instances of naked twins
    twins_candidate = [ box for box in values if len(values[box]) == 2 ]

    ##  # get all the naked pair twins ie exists twice in pairs
    nakedtwins = [[box_1, box_2] for box_1 in twins_candidate for box_2 in peers[box_1] if values[box_1]==values[box_2]]


    for i in range(len(nakedtwins)):
        paired_1 = nakedtwins[i][0] #  first box of paired
        paired_2 = nakedtwins[i][1] #  second one which has same element with 1st

        peers_of_1 = peers[paired_1] #  Find the peers
        peers_of_2 = peers[paired_2] #  Find the peers

        ## peer intesection
        peers_in_common = [ x for x in peers_of_1 if x in peers_of_2]

        ##  iterate through the naked_twins removing the values from the non naked twin boxes
        for peer in peers_in_common:
            if len(values[peer])>=2: # choose the peers which possible elements over 2
                for rm in values[paired_2]:
                    values = assign_value(values, peer, values[peer].replace(rm,''))
                    # Eliminate the naked twins as possibilities for their peers
    return values



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved = [ x for x in boxes if len(values[x])==1]
    for unit in solved:
        digit = values[unit]
        for i in peers[unit]:
            #values[i] = values[i].replace(digit,'')
            values = assign_value(values, i, values[i].replace(digit, ''))
    return values


def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            ans = [ x for x in unit if digit in values[x]]
            if len(ans) == 1:
                #values[ans[0]] = digit
                values = assign_value(values, ans[0], digit)
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = (solved_values_before == solved_values_after)
        if len([box for box in values if len(values[box]) == 0]):
            return False
    return values

def search(values):

    values = reduce_puzzle(values)

    if values is False:
        return False

    if all(len(values[s])==1 for s in boxes):
        return values

    _, s = min([ (len(values[i]), i) for i in values if len(values[i])>1 ])

    for i in values[s]:
        new_su = values.copy()
        new_su[s] = i

        attempt = search(new_su)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values


if __name__ == '__main__':

    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    #diag_sudoku_grid  = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    valid_cols_rows(cols, rows, diag_sudoku_grid)
    display(solve(diag_sudoku_grid))


    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

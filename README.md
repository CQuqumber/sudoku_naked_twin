# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint satisfaction is the process of finding a solution to a set of constraints that impose conditions that the variables must satisfy.
Ｗe apply naked twin strategy to reduce the possibilities in Sudoku.
	1. First, I idnetify all boxes which have only 2 possible vales.
	2. Trying to pair those have the same possible values and they are peers.
	3. Make sure each pair doesn't include the same box twice or we call make intersection.
	4. Remove those same possibilities.
Then, implement the naked_twins between eleminate and only_choice inside the function of reduce_puzzle.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The Simpliest way of mine is concating original unitlist to diagonal list.

```
## Two diagonal lists
diag_1 = [[rows[i]+cols[i] for i in range(len(cols))]]
diag_2 = [[rows[i]+cols[-i-1] for i in range(len(cols))]]
```

It will result in **TypeError** which Non-Diagonal design sudoku can't satisfy the constraints.

To solve both diagonal and non-diagonal, the forum mentor [suggest me](https://discussions.udacity.com/t/passes-local-test-but-fails-udacity-submit/292035/4) that **diagonal could be a boolean variable which would be true if we are solving for diagonal sudoku.**

```
diagonal = True
if diagonal:
    unitlist = row_units + column_units + square_units + diag_1 + diag_2
else:
    unitlist = row_units + column_units + square_units
```





### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

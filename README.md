# sat-solver

Run solver.py with any of the .cnf files as the second command line argument. You can also add a third command line argument which is the maximum number of variables to solve, since problems with more than 20 variables can take minutes to solve. Solver.py will generate a csv file, where each line is a different problem. 
 
You can then run ploy.py with an output file as the second command line argument to generate a scatter plot of problems by their number of variables and time to solve.

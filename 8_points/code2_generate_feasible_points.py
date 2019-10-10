import ast
import datetime
import pandas
import subprocess
from itertools import combinations, islice

index_combos = []

#Generating all possible combinations of points of sizes 2, 3 and 4
for size in [2, 3, 4]:
	if size !=4 :
		index_combos = index_combos + list(combinations(range(0, 8), size))
	
	else:
		index_combos = index_combos + list(islice(combinations(range(0, 8), 4), 35))


with open("all_point_sets.txt", "r") as ptsfile:
	allpts_str = ptsfile.readlines()

line_no = 1
for line in allpts_str:
	
	pointset_details = pandas.DataFrame()
	point_set = list(ast.literal_eval(line))

	optimals = [[], [], []]

	pointset_filename = "./feasible_point_sets/point_set_" + str(line_no)
	line_no += 1

	for indices in index_combos:

		combo_no = 1		
		remaining_indices = list(set(range(0, 8)).difference(indices))
		
		combo, remaining_points = [], []
		for index in indices:
			combo.append(point_set[index])
		
		for index in remaining_indices:
			remaining_points.append(point_set[index])

		#Generating .mod file for solving as LP
		for repeat in [1, 2]:
			
			lp_file = open("run.mod", "w")
			lp_file.write("var x1;\nvar x2;\n")
			lp_file.write("maximize obj: x1 + x2;\n")
			
			if repeat == 1:
				
				constraint_count = 1
				
				for coordinates in combo:

					to_print = "s.t. c" + str(constraint_count) + ": " + str(coordinates[0]) + " * x1 + " + str(coordinates[1]) + "* x2 >= 1;\n"
					lp_file.write(to_print)
					constraint_count += 1
				
				for coordinates in remaining_points:
					to_print = "s.t. c" + str(constraint_count) + ": " + str(coordinates[0]) + " * x1 + " + str(coordinates[1]) + "* x2 <= 1;\n"
					lp_file.write(to_print) 
					constraint_count += 1
				
				lp_file.write("solve;\nend;")
				lp_file.close()
					
			else:
				
				constraint_count = 1
				
				for coordinates in combo:
					to_print = "s.t. c" + str(constraint_count) + ": " + str(coordinates[0]) + " * x1 + " + str(coordinates[1]) + "* x2 <= 1;\n"
					lp_file.write(to_print)
					constraint_count += 1
				
				for coordinates in remaining_points:
					to_print = "s.t. c" + str(constraint_count) + ": " + str(coordinates[0]) + " * x1 + " + str(coordinates[1]) + "* x2 >= 1;\n"
					lp_file.write(to_print)
					constraint_count += 1

				lp_file.write("solve;\nend;")
				lp_file.close()
				
			#Using glpsol tool from GLPK GNU tool as python subprocess and checking for feasibility
			solving_LP = subprocess.run("glpsol --math run.mod > LP_result", shell = True)
			with open("LP_result", "r") as ptsfile:
				soln_LP = ptsfile.readlines()
			
			if ('NO' not in soln_LP[-4]):
				if combo not in optimals[0]:
					optimals[0].append(combo)
					optimals[1].append(len(combo))
					optimals[2].append(indices)

	if len(point_set) > len(optimals[0]):
		optimals[0].extend(['']*abs(len(point_set) - len(optimals[0])))
		optimals[1].extend(['']*abs(len(point_set) - len(optimals[0])))
		optimals[2].extend(['']*abs(len(point_set) - len(optimals[0])))
	
	else:
		point_set.extend(['']*abs(len(optimals[0]) - len(point_set)))
		
	pointset_details['PointSet'] = point_set
	pointset_details['Feasible_Set_Size'] = optimals[1]
	pointset_details['Feasible_Set_Indices'] = optimals[2]
	pointset_details['Feasible_Set_Points'] = optimals[0]
	
	pointset_details.to_csv(pointset_filename + ".csv", sep = ',', index = False)
	print (line_no, "\t at\t", datetime.datetime.now())
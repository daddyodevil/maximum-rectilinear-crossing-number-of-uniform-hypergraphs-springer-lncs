import ast
import pandas
import subprocess
from itertools import combinations
from datetime import datetime

start_time = datetime.now()

index_combos = []

all_colors = ['1110000', '1101000', '1100100', '1100010', '1100001', '1011000', '1010100', '1010010', '1010001', '1001100', '1001010', '1001001', '1000110', '1000101', '1000011', '0111000', '0110100', '0110010', '0110001', '0101100', '0101010', '0101001', '0100110', '0100101', '0100011', '0011100', '0011010', '0011001', '0010110', '0010101', '0010011', '0001110', '0001101', '0001011', '0000111']


with open("all_point_sets.txt", "r") as ptsfile:
	allpts_str = ptsfile.readlines()

for line in allpts_str:
	
	pointset_details = pandas.DataFrame()
	point_set = list(ast.literal_eval(line))
	lp_counter = 1
	
	for point_on_line in point_set:
		
		remaining_points = set(point_set).difference({point_on_line})
		#print ('On Line - ', point_on_line)
		#print ('Other - ', remaining_points)
		
		
		for combo_length in [1, 2, 3, 6]:
			
			for points_on_one_side in combinations(remaining_points, combo_length):
				
				points_on_other_side = list(remaining_points.difference(points_on_one_side))
				points_on_one_side = list(points_on_one_side)
				
				#print ('\nLength - ', len(points_on_one_side), '\n', points_on_one_side, '\n')
				
				for repeat in [1, 2]:
					
					lp_file = open("run" + str(lp_counter) +".mod", "w")
					lp_file.write("var x1;\nvar x2;\n")
					lp_file.write("maximize obj: x1 + x2;\n")
					lp_counter += 1
					constraint_count = 1
					
					to_print = "s.t. c" + str(constraint_count) + ": " + str(point_on_line[0]) + " * x1 + " + str(point_on_line[1]) + "* x2 = 1;\n"
					lp_file.write(to_print)
					constraint_count += 1
					
					if repeat == 1:
						
						for coordinates in points_on_one_side:
							to_print = "s.t. c" + str(constraint_count) + ": " + str(coordinates[0]) + " * x1 + " + str(coordinates[1]) + "* x2 >= 1;\n"
							lp_file.write(to_print)
							constraint_count += 1
					
						for coordinates in points_on_other_side:
							to_print = "s.t. c" + str(constraint_count) + ": " + str(coordinates[0]) + " * x1 + " + str(coordinates[1]) + "* x2 <= 1;\n"
							lp_file.write(to_print) 
							constraint_count += 1
							
					else:
						
						for coordinates in points_on_one_side:
							to_print = "s.t. c" + str(constraint_count) + ": " + str(coordinates[0]) + " * x1 + " + str(coordinates[1]) + "* x2 <= 1;\n"
							lp_file.write(to_print)
							constraint_count += 1
					
						for coordinates in points_on_other_side:
							to_print = "s.t. c" + str(constraint_count) + ": " + str(coordinates[0]) + " * x1 + " + str(coordinates[1]) + "* x2 >= 1;\n"
							lp_file.write(to_print) 
							constraint_count += 1
					
					lp_file.write("solve;\nend;")
					lp_file.close()
					
					solving_LP = subprocess.run("glpsol --math run.mod > LP_result", shell = True)
			with open("LP_result", "r") as ptsfile:
					soln_LP = ptsfile.readlines()
				
					#if ('NO' not in soln_LP[-4]):
						#print ('found')
					
					
					
					

end_time = datetime.now()

print ('START - ', start_time, '\nEND - ', end_time, 'DIFFERENCE - ', start_time - end_time)






'''
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
'''
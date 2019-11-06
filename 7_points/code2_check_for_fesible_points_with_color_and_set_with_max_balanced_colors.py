from itertools import combinations
from datetime import datetime
import ast
import json
import numpy
import pandas
import subprocess

start_time = datetime.now()

all_colors = ['1110000', '1101000', '1100100', '1100010', '1100001', '1011000', '1010100', '1010010', '1010001', '1001100', '1001010', '1001001', '1000110', '1000101', '1000011', '0111000', '0110100', '0110010', '0110001', '0101100', '0101010', '0101001', '0100110', '0100101', '0100011', '0011100', '0011010', '0011001', '0010110', '0010101', '0010011', '0001110', '0001101', '0001011', '0000111']

balanced_color_counter = {}
max_color_counter = {}

with open("all_point_sets.txt", "r") as ptsfile:
	allpts_str = ptsfile.readlines()

point_set_counter = 1
for line in allpts_str:
	
	pointset_details = pandas.DataFrame()
	point_set = list(ast.literal_eval(line))
	#print ('Point Set -\n', point_set)
	final_result, colors, points_on_line, points_in_first_halfspace, points_in_second_halfspace, results, checked_set = [], [], [], [], [], [], []
	
	for color in all_colors:
		balanced_color_counter[color] = 0
	
	point_indices = list(range(7))

	for index_of_point_on_line in point_indices:

		other_indices = [index for index in point_indices if index != index_of_point_on_line]

		for combo_length in [0, 1, 2, 3]:
			
			for index_of_points_on_one_side in combinations(other_indices, combo_length):
				
				points_on_other_side = [point_set[index] for index in other_indices if index not in index_of_points_on_one_side]
				points_on_one_side = [point_set[index] for index in index_of_points_on_one_side]
				point_on_line = point_set[index_of_point_on_line]
				
				if (points_on_one_side not in checked_set or points_on_other_side not in checked_set):
					
					checked_set.append(points_on_one_side)
					checked_set.append(points_on_other_side)

					for repeat in [1, 2]:
						
						lp_file = open("lp_file.mod", "w")
						lp_file.write("var x1;\nvar x2;\n")
						lp_file.write("maximize obj: x1 + x2;\n")
						constraint_count = 1
						
						to_print = "s.t. c" + str(constraint_count) + ": " + str(point_on_line[0]) + " * x1 + " + str(point_on_line[1]) + "* x2 = 1;\n"
						lp_file.write(to_print)
						constraint_count += 1
						
						if repeat != 1:
							points_on_one_side, points_on_other_side = points_on_other_side, points_on_one_side
							
							
						for coordinates in points_on_one_side:
							to_print = "s.t. c" + str(constraint_count) + ": " + str(coordinates[0]) + " * x1 + " + str(coordinates[1]) + "* x2 >= 1;\n"
							lp_file.write(to_print)
							constraint_count += 1
					
						for coordinates in points_on_other_side:
							to_print = "s.t. c" + str(constraint_count) + ": " + str(coordinates[0]) + " * x1 + " + str(coordinates[1]) + "* x2 <= 1;\n"
							lp_file.write(to_print) 
							constraint_count += 1
						
						lp_file.write("solve;\nend;")
						lp_file.close()
						
						solving_LP = subprocess.run("glpsol --math lp_file.mod > LP_result", shell = True)
						with open("LP_result", "r") as ptsfile:
							soln_LP = ptsfile.readlines()
							
						if ('NO' not in soln_LP[-4]):
							for color in all_colors:
								
								point_on_line_color = color[point_set.index(point_on_line)]
								points_on_one_side_color = ''
								points_on_other_side_color = ''
								result = ''
								
								for coordinates in points_on_one_side:
									points_on_one_side_color += color[point_set.index(coordinates)]
								
								for coordinates in points_on_other_side:
									points_on_other_side_color += color[point_set.index(coordinates)]							
								
								if point_on_line_color == '0':
									
									if points_on_one_side_color.count('1') == 3 or points_on_one_side_color.count('1') == 3:
										result = 'I'
										
									elif len(points_on_one_side_color) == 0 or len(points_on_other_side_color) == 0:
										result = 'B'
										balanced_color_counter[color] += 1
										
									elif len(points_on_one_side_color) == 2 and points_on_one_side_color.count('0') == 1:
										result = 'B'
										balanced_color_counter[color] += 1
									
									elif len(points_on_other_side_color) == 2 and points_on_other_side_color.count('0') == 1:
										result = 'B'
										balanced_color_counter[color] += 1
									
									else:
										result = 'I'
								
								elif point_on_line_color == '1':
									
									if len(points_on_one_side_color) == 2 and points_on_one_side_color.count('1') == 2:
										result = 'I'
									
									elif len(points_on_other_side_color) == 2 and points_on_other_side_color.count('1') == 2:
										result = 'I'
									
									elif len(points_on_one_side_color) == 1 and points_on_one_side_color == '0':
										result = 'B'
										balanced_color_counter[color] += 1
									
									elif len(points_on_other_side_color) == 1 and points_on_other_side_color == '0':
										result = 'B'
										balanced_color_counter[color] += 1
										
									elif len(points_on_one_side_color) == len(points_on_other_side_color):
										
										if points_on_one_side_color.count('1') == 1:
											result = 'B'
											balanced_color_counter[color] += 1
											
										else:
											result = 'I'
											
									else:
										result = 'I'
																
								colors.append(color)
								points_on_line.append(str(point_on_line) + ' - ' + point_on_line_color)
								points_in_first_halfspace.append(str(points_on_one_side) + ' - ' + points_on_one_side_color)
								points_in_second_halfspace.append(str(points_on_other_side) + ' - ' + points_on_other_side_color)
								results.append(result)
								
							break
							
	all_values = [point_set, colors, points_on_line, points_in_first_halfspace, points_in_second_halfspace, results]
	
	for item_list in all_values:
		
		if len(all_values[1]) > len(item_list):
			item_list.extend(['']*abs(len(all_values[1]) - len(item_list)))
		
		else:
			item_list.extend(['']*abs(len(item_list) - len(all_values[1])))		
		
		final_result.append(item_list)
	
	pandas.DataFrame(numpy.transpose(final_result)).sort_values(by = [1, 5]).to_csv("PT_SET_" + str(point_set_counter) + ".csv", sep = ',', index = False)
	
	with open("BALANCED_SETS_FOR_PT_SET_" + str(point_set_counter) + ".json", 'w') as balanced_color_file:
		json.dump(balanced_color_counter, balanced_color_file)
	
	max_color_counter["PT_SET_" + str(point_set_counter) + "_with_color_" + str(max(balanced_color_counter, key = balanced_color_counter.get))] = balanced_color_counter[max(balanced_color_counter, key = balanced_color_counter.get)]
	point_set_counter += 1

for ptset in max_color_counter:
	print (ptset, '\t-\t', max_color_counter[ptset])

print (max(max_color_counter, key = max_color_counter.get), '\t-\t', max_color_counter[max(max_color_counter, key = max_color_counter.get)])

end_time = datetime.now()
print ('\nSTART_TIME - ', start_time, '\nEND_TIME - ', end_time, '\nTOTAL_TIME_TAKEN - ', end_time - start_time)
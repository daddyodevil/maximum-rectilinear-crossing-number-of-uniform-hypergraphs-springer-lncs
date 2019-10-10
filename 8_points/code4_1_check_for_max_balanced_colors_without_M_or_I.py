from ast import literal_eval
import numpy
import pandas

total_set_size, balanced_sets_found = [], [[], []]
balanced_set_counter = 0

for file_no in range(1, 3316):
	
	file_name = "./feasible_point_sets/point_set_" + str(file_no) + "_with_color_check.csv"

	if (type(file_name) == 'bytes'):
		feasible_ptset = pandas.read_csv(file_name.decode('utf-8'))
	else:
		feasible_ptset = pandas.read_csv(file_name)
	
	size_of_all_feasible_sets = feasible_ptset['Feasible_Set_Size'].values.tolist()

	required_colors = ['00001111', '00010111', '00011011', '00011101', '00011110', '00100111', '00101011', '00101101', '00101110', '00110011', '00110101', '00110110', '00111001', '00111010', '00111100', '01000111', '01001011', '01001101', '01001110', '01010011', '01010101', '01010110', '01011001', '01011010', '01011100', '01100011', '01100101', '01100110', '01101001', '01101010', '01101100', '01110001', '01110010', '01110100', '01111000', '10000111', '10001011', '10001101', '10001110', '10010011', '10010101', '10010110', '10011001', '10011010', '10011100', '10100011', '10100101', '10100110', '10101001', '10101010', '10101100', '10110001', '10110010', '10110100', '10111000', '11000011', '11000101', '11000110', '11001001', '11001010', '11001100', '11010001', '11010010', '11010100', '11011000', '11100001', '11100010', '11100100', '11101000', '11110000']

	for color in required_colors:
		one_side_color = feasible_ptset[color].values.tolist()
		
		monochrome_found = 0
		for index in range(0, len(size_of_all_feasible_sets)):

			if size_of_all_feasible_sets[index] == 2 or size_of_all_feasible_sets[index] == 3:
				if ('M' in one_side_color[index]):
					monochrome_found = 1
					break
			elif size_of_all_feasible_sets[index] == 4:
				if ('M' in one_side_color[index] or 'I' in one_side_color[index]):
					monochrome_found = 1
					break
		
		if monochrome_found == 0:
			
			point_set = [literal_eval(ptset) for ptset in feasible_ptset['PointSet'].values.tolist()[:8]]
			
			if point_set not in balanced_sets_found[0]:
				
				balanced_sets_found[0].append([point for point in point_set])
				balanced_sets_found[1].append(color)
				balanced_set_counter += 1
				
				feasible_indices_2set_4set = [literal_eval(ptset) for ptset in feasible_ptset['Feasible_Set_Indices'].values.tolist()[:-1] if len(literal_eval(ptset))!=3]
				feasible_points_2set_4set = [literal_eval(ptset) for ptset in feasible_ptset['Feasible_Set_Points'].values.tolist()[:-1] if len(literal_eval(ptset))!=3]
				colors = [entry for entry in feasible_ptset[color].values.tolist()[:-1] if entry.find(' ') !=3]
				total_set_size = [feasible_ptset[color].values.tolist()[-1]]
				
				balanced_color = [color, color.replace('0', 'color').replace('1', '0').replace('color', '1')]
				
				point_set.extend(['']*abs(len(feasible_indices_2set_4set) - len(point_set)))
				balanced_color.extend([''] * abs(len(feasible_indices_2set_4set) - len(total_set_size) - 1))
				total_set_size.extend([''] * abs(len(feasible_indices_2set_4set) - len(total_set_size)))
				
				balanced_set_details = [point_set, feasible_indices_2set_4set, colors, balanced_color, total_set_size]
				balanced_set_details = numpy.asarray(balanced_set_details).transpose()
				
				single_balanced_ptset = pandas.DataFrame(balanced_set_details)
				single_balanced_ptset.columns = ['Point_Set', 'Feasible_Set_Indices_2set_4set', 'Index_Colors_2set_4set', 'Complete_Set_Color', 'Total_Balanced']
				single_balanced_ptset.to_csv('./max_feasible/Balanced_Set_' + str(balanced_set_counter) + '.csv', sep = ',', index = False)

			
			else:
				for index in range(0, len(balanced_sets_found[0])):
					if point_set == balanced_sets_found[0][index]:
						
						ptset_color = balanced_sets_found[1][index]
					
						if color != ptset_color.replace('0', 'ptset_color').replace('1', '0').replace('ptset_color', '1'):
							
							balanced_sets_found[0].append([point for point in point_set])
							balanced_sets_found[1].append(color)
							balanced_set_counter += 1
							
							feasible_indices_2set_4set = [literal_eval(ptset) for ptset in feasible_ptset['Feasible_Set_Indices'].values.tolist()[:-1] if len(literal_eval(ptset))!=3]
							feasible_points_2set_4set = [literal_eval(ptset) for ptset in feasible_ptset['Feasible_Set_Points'].values.tolist()[:-1] if len(literal_eval(ptset))!=3]
							colors = [entry for entry in feasible_ptset[color].values.tolist()[:-1] if entry.find(' ') !=3]
							total_set_size = [feasible_ptset[color].values.tolist()[-1]]
							
							balanced_color = [color, color.replace('0', 'color').replace('1', '0').replace('color', '1')]
							
							point_set.extend(['']*abs(len(feasible_indices_2set_4set) - len(point_set)))
							balanced_color.extend([''] * abs(len(feasible_indices_2set_4set) - len(total_set_size) - 1))
							total_set_size.extend([''] * abs(len(feasible_indices_2set_4set) - len(total_set_size)))
							
							balanced_set_details = [point_set, feasible_indices_2set_4set, colors, balanced_color, total_set_size]
							balanced_set_details = numpy.asarray(balanced_set_details).transpose()
							
							single_balanced_ptset = pandas.DataFrame(balanced_set_details)
							single_balanced_ptset.columns = ['Point_Set', 'Feasible_Set_Indices_2set_4set', 'Index_Colors_2set_4set', 'Complete_Set_Color', 'Total_Balanced']
							single_balanced_ptset.to_csv('./max_feasible/Balanced_Set_' + str(balanced_set_counter) + '.csv', sep = ',', index = False)
import os
import pandas

directory = "./feasible_point_sets/"
files = os.listdir(directory)
print (len(files))

#The list of 70 possible colors with equal number of points of both colors
required_colors = ['00001111', '00010111', '00011011', '00011101', '00011110', '00100111', '00101011', '00101101', '00101110',
				   '00110011', '00110101', '00110110', '00111001', '00111010', '00111100', '01000111', '01001011', '01001101',
				   '01001110', '01010011', '01010101', '01010110', '01011001', '01011010', '01011100', '01100011', '01100101',
				   '01100110', '01101001', '01101010', '01101100', '01110001', '01110010', '01110100', '01111000', '10000111',
				   '10001011', '10001101', '10001110', '10010011', '10010101', '10010110', '10011001', '10011010', '10011100',
				   '10100011', '10100101', '10100110', '10101001', '10101010', '10101100', '10110001', '10110010', '10110100',
				   '10111000', '11000011', '11000101', '11000110', '11001001', '11001010', '11001100', '11010001', '11010010',
				   '11010100', '11011000', '11100001', '11100010', '11100100', '11101000', '11110000']

for file in files:
	
	file_name = directory + file
	feasible_ptset = pandas.read_csv(file_name)
	row_to_add = ["", "", "", "Total Balanced Sets"]
	
	feasible_indices_str = list(feasible_ptset['Feasible_Set_Indices'])
	feasible_indices = [eval(feasible_indices_str[index]) for index in range(len(feasible_indices_str))]
	for color in required_colors:
		
		color_result = []
		balance_counter = 0
		
		for indices in feasible_indices:
			setsize = len(indices)
			
			#If the number of points is two then the possiblites are either both are of same color i.e. it is monochromatic or two points are of different colors, i.e. equal number of points of each color, therefore balanced
			if setsize == 2:
				one_side_color = color[indices[0]] + color [indices[1]]
				if one_side_color.count('1') == 1:
					color_result.append(one_side_color + " - B")
					balance_counter += 1
				else:
					color_result.append(one_side_color + " - M")
					
			#If the number of points are three then there are two possiblites, they all are of same color i.e. monochromatic or two points are of same color and the other one is different, i.e. they are imbalanced
			elif setsize == 3:
				one_side_color = color[indices[0]] + color [indices[1]] + color[indices[2]]
				if one_side_color.count('1') == 2 or one_side_color.count('0') == 2:
					color_result.append(one_side_color + " - I")
				elif one_side_color.count('1') == 3 or one_side_color.count('0') == 3:
					color_result.append(one_side_color + " - M")
			
			#If the number of points are four then there are four possiblites, they all are of same color i.e. monochromatic or two points are of same color and the other two are same, i.e. they are balanced and lastly threee are of the same color and one is different i.e. imbalanced
			elif setsize == 4:
				one_side_color = color[indices[0]] + color [indices[1]] + color[indices[2]] + color[indices[3]]
				if one_side_color.count('1') == 2:
					color_result.append(one_side_color + " - B")
					balance_counter += 1
				elif one_side_color.count('1') == 1 or one_side_color.count('0') == 1:
					color_result.append(one_side_color + " - I")
				elif one_side_color.count('1') == 0 or one_side_color.count('1') == 4:
					color_result.append(one_side_color + " - M")
		
		feasible_ptset[color] = color_result
		row_to_add.append(balance_counter)
		
	feasible_ptset.loc[-1] = row_to_add
	
	file_name = file_name[:-4] + "_with_color_check.csv"
	feasible_ptset.to_csv(file_name, sep = ',', index = False)
	
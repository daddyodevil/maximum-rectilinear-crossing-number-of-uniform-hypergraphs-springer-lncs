global colors
colors = []

def gen_color(size, current_string , no_of_ones):
	
	global colors
	
	if (size == 1):
		
		if (no_of_ones == 2):
			final_string = current_string + '1'
			colors.append(final_string)
		
		elif (no_of_ones == 2 or no_of_ones == 3):
			final_string = current_string + '0'
			colors.append(final_string)
		
		return
	
	else:
		
		if (no_of_ones < 3):
			new_string = current_string + '1'
			gen_color(size - 1, new_string, no_of_ones + 1)
		
			new_string = current_string + '0'
			gen_color(size - 1, new_string, no_of_ones)
		
		else:
			new_string = current_string + '0'
			gen_color(size - 1, new_string, no_of_ones)
		
		

gen_color(7, '', 0)

print ('LIST OF COLORS - \n', colors, '\n')
print ('NUMBER OF COLORS - ', len(colors), '\n')
#Reading the file and saving it as a list of strings
with open("raw_points.txt", "r") as rawfile:
    rawlines = rawfile.readlines()

all_point_coordinates = [[]]

for line in rawlines:
	if '-' not in line:
		all_point_coordinates[-1].append(tuple(map(int, line.split())))
		
	else:
		all_point_coordinates.append([])
		
with open("all_point_sets.txt", "w") as point_set_file:
	for point_set in all_point_coordinates:
		for index in range(0, len(point_set)):
			if (index!=6):
				point_set_file.write(str(point_set[index]) + ", ")
			else:
				point_set_file.write(str(point_set[index]) + "\n")
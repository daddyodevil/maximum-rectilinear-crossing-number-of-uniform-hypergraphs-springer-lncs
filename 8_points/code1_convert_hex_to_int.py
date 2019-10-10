#Reading the file and saving it as a list of strings
with open("./point_set_hex.txt", "r") as hexfile:
    hexlines = hexfile.readlines()
        
all_point_coordinates = []

for line in hexlines:
    
    #Splitting the line into list of coordinates, still as a string
    point_set = []        
    points = line.split()
    
    for point in points:
        
        #Convertng points from hexadecimal string into ints
        x_coord = int(point[0:2], 16)
        y_coord = int(point[2:], 16)
        
        point_set.append((x_coord, y_coord))
                
    all_point_coordinates.append(list(point_set))
    
#Saving list of points in integer format to a file

with open("all_point_sets.txt", "w") as point_set_file:
    for point_set in all_point_coordinates:
        for point in point_set:
            point_set_file.write(str(point) + ", ")
        
        point_set_file.write("\n")
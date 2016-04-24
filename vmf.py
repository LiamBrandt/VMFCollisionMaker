GLOBAL = {
	"global_id": 0,
}

class VMF(object):
	def __init__(self):
		self.properties = {
			"versioninfo": VersionInfo(),
			"visgroups": VisGroups(),
			"world": World(),
			"cameras": Cameras(),
			"cordon": Cordon(),
		}
		
class VersionInfo(object):
	def __init__(self):
		self.properties = {
			"editorversion": "400",
			"editorbuild": "6412",
			"mapversion": "0",
			"formatversion": "100",
			"prefab": "0",
		}
		
class VisGroups(object):
	def __init__(self):
		self.properties = {}
		
class World(object):
	def __init__(self):
		self.properties = {
			"id": get_unique_id(),
			"mapversion": "1",
			"classname": "worldspawn",
			"skyname": "sky_wasteland02",
			"solid": [],
		}
	
	def add_solid(self, pos, size, displacement=None):
		new_solid = Solid()
		far = (pos[0]+size[0], pos[1]+size[1], pos[2]+size[2])
		
		uaxis = []
		uaxis.append("[1 0 0 0] 0.25")
		uaxis.append("[1 0 0 0] 0.25")
		uaxis.append("[0 1 0 0] 0.25")
		uaxis.append("[0 1 0 0] 0.25")
		uaxis.append("[1 0 0 0] 0.25")
		uaxis.append("[1 0 0 0] 0.25")
		
		vaxis = []
		vaxis.append("[0 -1 0 0] 0.25")
		vaxis.append("[0 -1 0 0] 0.25")
		vaxis.append("[0 0 -1 0] 0.25")
		vaxis.append("[0 0 -1 0] 0.25")
		vaxis.append("[0 0 -1 0] 0.25")
		vaxis.append("[0 0 -1 0] 0.25")
		
		planes = []
		planes.append( [[0, 0, 1], [0, 1, 1], [1, 1, 1]] )
		planes.append( [[0, 1, 0], [0, 0, 0], [1, 0, 0]] )
		planes.append( [[0, 0, 0], [0, 1, 0], [0, 1, 1]] )
		planes.append( [[1, 1, 0], [1, 0, 0], [1, 0, 1]] )
		planes.append( [[0, 1, 0], [1, 1, 0], [1, 1, 1]] )
		planes.append( [[1, 0, 0], [0, 0, 0], [0, 0, 1]] )
		
		side_index = -1
		for each_plane in planes:
			side_index += 1
			current_plane = ""
			for each_point in each_plane:
				current_plane += "("
				number_index = -1
				for each_number in each_point:
					number_index += 1
					if each_number == 0:
						point_number = str(pos[number_index])
					else:
						point_number = str(far[number_index])
					#omit space before parentheses
					if number_index != 2:
						current_plane += point_number + " "
					else:
						current_plane += point_number
				current_plane += ") "
					
			new_solid.add_side(current_plane, uaxis[side_index], vaxis[side_index])
		
		if displacement != None:
			new_solid.properties["side"][0].properties["dispinfo"].append(displacement)
		
		self.properties["solid"].append(new_solid)
		
class Solid(object):
	def __init__(self):
		self.properties = {
			"id": get_unique_id(),
			"side": [],
			"editor": Editor(),
		}
		
	def add_side(self, plane, uaxis, vaxis):
		new_side = Side()
		new_side.properties["plane"] = plane
		new_side.properties["uaxis"] = uaxis
		new_side.properties["vaxis"] = vaxis
		
		self.properties["side"].append(new_side)
		
class Side(object):
	def __init__(self):
		self.properties = {
			"id": get_unique_id(),
			"plane": "(512 -512 -512) (-512 -512 -512) (-512 -512 512)",
			"material": "BRICK/BRICKFLOOR001A",
			"uaxis": "[1 0 0 0] 0.25",
			"vaxis": "[0 0 -1 0] 0.25",
			"rotation": "0",
		    "lightmapscale": "16",
			"smoothing_groups": "0",
			"dispinfo": [],
		}
		
	def add_displacement(self, power, pos):
		new_displacement = DispInfo(power, pos)
		
		self.properties["dispinfo"].append(new_displacement)
		
class DispInfo(object):
	def __init__(self, power, pos):
		self.properties = {
			"power": str(power),
			"startposition": "[" + str(pos[0]) + " " + str(pos[1]) + " " + str(pos[2]) + "]",
			"elevation": "0",
			"subdiv": "0",
			"normals": Normals(power),
			"distances": Distances(power),
			"offsets": Offsets(power),
			"offset_normals": OffsetNormals(power),
			"alphas": Alphas(power),
			"triangle_tags": TriangleTags(power),
			"allowed_verts": AllowedVerts(power),
		}
		
class Normals(object):
	def __init__(self, power):
		self.properties = {}
		
		vertex_width = (2 ** power) + 1
		
		print("Normals Created")
		
		#go through each row
		for each_row in range(vertex_width):
			row_value = ""
			#each number in the row is either 0 or 1, every 3rd entry is 1 for the z axis normal
			for number_index in range(vertex_width*3):
				if (number_index+1) % 3 == 0:
					row_value += "1 "
				else:
					row_value += "0 "
			self.properties["row" + str(each_row)] = row_value
			
class Distances(object):
	def __init__(self, power):
		self.properties = {}
		
		vertex_width = (2 ** power) + 1
		
		for each_row in range(vertex_width):
			self.properties["row" + str(each_row)] = "0 " * vertex_width
		
class Offsets(object):
	def __init__(self, power):
		self.properties = {}
		
		vertex_width = (2 ** power) + 1
		
		for each_row in range(vertex_width):
			self.properties["row" + str(each_row)] = "0 " * vertex_width*3
			
class OffsetNormals(object):
	def __init__(self, power):
		self.properties = {}
		
		vertex_width = (2 ** power) + 1
		
		for each_row in range(vertex_width):
			self.properties["row" + str(each_row)] = "0 " * vertex_width*3
			
class Alphas(object):
	def __init__(self, power):
		self.properties = {}
		
		vertex_width = (2 ** power) + 1
		
		for each_row in range(vertex_width):
			self.properties["row" + str(each_row)] = "0 " * vertex_width
			
class TriangleTags(object):
	def __init__(self, power):
		self.properties = {}
		
		vertex_width = (2 ** power) + 1
		
		for each_row in range(vertex_width-1):
			self.properties["row" + str(each_row)] = "9 " * (vertex_width-1)*2
		
class AllowedVerts(object):
	def __init__(self, power):
		self.properties = {
			"10": "-1 -1 -1 -1 -1 -1 -1 -1 -1 -1",
		}
		
class Editor(object):
	def __init__(self):
		self.properties = {
			"color": "0 200 0",
			"visgroupshown": "1",
			"visgroupautoshown": "1",
		}
		
class Cameras(object):
	def __init__(self):
		self.properties = {
			"activecamera": "-1",
		}
		
class Cordon(object):
	def __init__(self):
		self.properties = {
			"mins": "(-1024 -1024 -1024)",
			"maxs": "(1024 1024 1024)",
			"active": "0",
		}
			
def get_unique_id():
	GLOBAL["global_id"] += 1
	return str(GLOBAL["global_id"])
	
def write_properties(file, property_object, indent=0):
	#print(indent)
	#print(str(property_object))
	file.truncate()
	
	prop_dict = property_object.properties
	for each_key in prop_dict:
		#print(type(prop_dict[each_key]))
		
		#STRINGS
		if type(prop_dict[each_key]) == types.StringType:
			#print(prop_dict[each_key])
			file.write('\t'*indent + '"' + each_key + '" "' + prop_dict[each_key] + '"\n')
			
		#VARIABLE AMOUNT OF OBJECTS (LIST OF OBJECTS)
		elif type(prop_dict[each_key]) == types.ListType:
			for each_object in prop_dict[each_key]:
				file.write('\t'*indent + each_key + '\n')
				file.write('\t'*indent + "{\n")
				indent += 1
				write_properties(file, each_object, indent)
				indent -= 1
				file.write('\t'*indent + '}\n')
			
		#OBJECTS
		else:
			file.write('\t'*indent + each_key + '\n')
			file.write('\t'*indent + "{\n")
			indent += 1
			write_properties(file, prop_dict[each_key], indent)
			indent -= 1
			file.write('\t'*indent + '}\n')
		
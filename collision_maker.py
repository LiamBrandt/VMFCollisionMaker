import pygame, sys, traceback, random

from vmf import *

pygame.init()

SETTINGS = {}

with open('config.txt','r') as inf:
    SETTINGS = eval(inf.read()) 

pygame.display.set_icon(pygame.image.load("content/icon.png"))
screen = pygame.display.set_mode([SETTINGS["resolution_x"], SETTINGS["resolution_y"]])
	
pygame.display.set_caption("VMF Collision Maker")
	
INFO = {
	"x_offset": 0,
	"y_offset": 0,
	
	"zoom": 1,
	
	"font_size": 34,
	"text_pos": 0,
}
INFO["normal_font"] = pygame.font.Font("content/Helvetica.ttf", INFO["font_size"])

COLORS = {}

def trace_crash(msg):
	if SETTINGS["debug"] == True:
		log_file = open("crash_log.txt", "a")
		log_file.write(str(msg) + "\n")
		print(str(msg))
		log_file.close()
		
		
class Island(object):
	def __init__(self):
		self.vertices = []
		self.faces = []
		
	def find_face_vertices(self):
		old_percent = 0
		
		face_number = 0
		for each_face in self.faces:
			face_number += 1
			for each_vert_id in each_face.vert_ids:
				for each_vertice in self.vertices:
					if each_vertice.id == each_vert_id:
						each_face.verts.append(each_vertice)
						
						#print(float(face_number) / len(self.faces))
						percent = int((float(face_number) / len(self.faces)) * 100)
						#print(percent)
						if percent != old_percent:
							old_percent = percent
							print(str(percent) + "%")
		
	"""def find_closest_vertice(self, pos):
		closest = [999999, 999999, 999999, 999999]
		closest_vertice = [None, None, None, None]
		for each_vertice in self.vertices:
			#2d distance formula
			distance = ( (each_vertice.x - pos[0])**2 + (each_vertice.z - pos[2])**2 ) ** (0.5)
			for closest_index in range(len(closest)):
				if distance < closest[closest_index]:
					closest[closest_index] = distance
					closest_vertice[closest_index] = each_vertice
			
		highest = 0
		for each_vertice in closest_vertice:
			if each_vertice.y > highest:
				highest = each_vertice.y
			
		return int(highest)"""
		
	def find_closest_vertice(self, pos):
		closest = 999999
		closest_vertice = None
		for each_vertice in self.vertices:
			#2d distance formula
			distance = ( (each_vertice.x - pos[0])**2 + (each_vertice.z - pos[2])**2 ) ** (0.5)
			if distance < closest:
				closest = distance
				closest_vertice = each_vertice
				
		return closest_vertice.y

		
	def draw(self):
		screen.fill([0, 0, 0])
	
		#for each_vertice in self.vertices:
		#	each_vertice.draw()
			
		for each_face in self.faces:
			each_face.draw()
			
		width = (2**SETTINGS["power"]) * SETTINGS["size"]
		
		y = 0
		for each_row in range(width):
			x = 0
			for each_disp in range(width):
				draw_x = (x+SETTINGS["x_offset"]+INFO["x_offset"])*INFO["zoom"] + (SETTINGS["resolution_x"]/2)
				draw_y = (y+SETTINGS["y_offset"]+INFO["y_offset"])*INFO["zoom"] + (SETTINGS["resolution_y"]/2)
				size = int(SETTINGS["increment"]*INFO["zoom"])
				#print("draw at: " + str(draw_x) + ", " + str(draw_y))
				pygame.draw.rect(screen, (0, 255, 255), [int(draw_x), int(draw_y), size, size], 1)
				x += SETTINGS["increment"]
			y += SETTINGS["increment"]
			
			
		#pygame.draw.rect(screen, (255, 0, 255), [-512+INFO["x_offset"], -512+INFO["y_offset"], 256, 256], 4)
		#pygame.draw.rect(screen, (255, 0, 255), [256+INFO["x_offset"], 256+INFO["y_offset"], 256, 256], 4)	

class Face(object):
	def __init__(self, vert_ids, group):
		self.vert_ids = vert_ids
		self.group = group
		
		self.color = (255, 255, 255)
		
		self.verts = []
		
	def update_color(self):
		self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		try:
			if SETTINGS["random_colors"] == False:
				self.color = COLORS[str(self.group)]
		except:
			pass

		
	def draw(self):
		points = []
		for index in range(3):
			draw_point = project([self.verts[index].x, self.verts[index].z])
			points.append(draw_point)
		
		#only draw polygon if a vertice is on the screen
		for each_point in points:
			if each_point[0] < SETTINGS["resolution_x"] and each_point[0] > 0:
				if each_point[1] < SETTINGS["resolution_y"] and each_point[1] > 0:
					pygame.draw.polygon(screen, self.color, points, 0)
					break
			
class Vertice(object):
	def __init__(self, x, y, z, id):
		self.x = x
		self.y = y
		self.z = z
		self.id = id
		
	def draw(self):
		draw_x = self.x + INFO["x_offset"]
		draw_y = self.y + INFO["y_offset"]
		
		pygame.draw.rect(screen, (255, 255, 255), (draw_x, draw_y, 2, 2), 0)
			
			
def add_displacement(vmf, island, pos, size, scale):
	power = SETTINGS["power"]
	displacement = DispInfo(power, [pos[0], pos[1], pos[2]])
	
	increment = scale
	
	#fill dispinfo distances with island vertice data
	y = pos[1]
	for row_index in range((2 ** power)+1):
		y += increment
		x = pos[0]
		row_value = ""
		for number_index in range((2 ** power)+1):
			x += increment
			#closest_vertice = island.find_closest_vertice([-x, 0, y])
			closest_vertice = island.find_closest_vertice([x, 0, y])

			row_value += str(closest_vertice) + " "
	
		displacement.properties["distances"].properties["row" + str(row_index)] = row_value

	vmf.properties["world"].add_solid(pos, size, displacement)
		
def project(point):
	x = (point[0]+INFO["x_offset"])*INFO["zoom"]+(SETTINGS["resolution_x"]/2)
	y = (point[1]+INFO["y_offset"])*INFO["zoom"]+(SETTINGS["resolution_y"]/2)
	return [x, y]
		
def add_text(text):
	text_surface = INFO["normal_font"].render(text, True, (255, 255, 255))
	shadow = INFO["normal_font"].render(text, True, (0, 0, 0))
	
	screen.blit(shadow, [3, INFO["text_pos"]+3])
	screen.blit(text_surface, [0, INFO["text_pos"]])
	
	INFO["text_pos"] += INFO["font_size"]
		
def main():
	island = Island()

	#READ OBJ FILE
	obj_file = open("land.obj", "r")
	
	current_vert_id = 0
	current_group = 0
	
	reading = True
	while(reading):
		new_line = obj_file.readline()
		if new_line == "":
			reading = False
			break
		
		new_line = new_line[:-1]
		vertex = new_line.split()
		#skip newlines
		if vertex != []:
			#VERTS
			if vertex[0] == "v":
				current_vert_id += 1
				x = int(float(vertex[1])) * SETTINGS["global_scale"]
				y = int(float(vertex[2])) * SETTINGS["global_scale"]
				z = -int(float(vertex[3])) * SETTINGS["global_scale"]
				island.vertices.append(Vertice(x, y, z, current_vert_id))
			
			#FACES
			elif vertex[0] == "f":
				vert_id_1 = int(vertex[1].split("/")[0])
				vert_id_2 = int(vertex[2].split("/")[0])
				vert_id_3 = int(vertex[3].split("/")[0])
				island.faces.append(Face([vert_id_1, vert_id_2, vert_id_3], current_group))
				
			#GROUPS
			if SETTINGS["random_colors"] == False:
				if vertex[0] == "g":
					current_group = vertex[1]
					COLORS[str(current_group)] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		
	obj_file.close()
			
	for each_face in island.faces:
		each_face.update_color()
			
			
	#CREATE ISLAND FACES FROM RAW OBJ DATA
	island.find_face_vertices()
			
	#DO PYGAME STUFF
	while(True):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
				
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 5:
					if INFO["zoom"] > 0.01:
						INFO["zoom"] = INFO["zoom"] * 0.5
				elif event.button == 4:
					if INFO["zoom"] < 1024:
						INFO["zoom"] = INFO["zoom"] * 2
				
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					SETTINGS["y_velocity"] = 0
				if event.key == pygame.K_DOWN:
					SETTINGS["y_velocity"] = 0
				if event.key == pygame.K_LEFT:
					SETTINGS["x_velocity"] = 0
				if event.key == pygame.K_RIGHT:
					SETTINGS["x_velocity"] = 0
				
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					SETTINGS["y_velocity"] = -1
				if event.key == pygame.K_DOWN:
					SETTINGS["y_velocity"] = 1
				if event.key == pygame.K_LEFT:
					SETTINGS["x_velocity"] = -1
				if event.key == pygame.K_RIGHT:
					SETTINGS["x_velocity"] = 1
					
				if event.key == pygame.K_w:
					SETTINGS["increment"] += 0.2
				if event.key == pygame.K_s:
					if SETTINGS["increment"] > 0.2:
						SETTINGS["increment"] -= 0.2
				
				if event.key == pygame.K_a:
					if SETTINGS["size"] > 1:
						SETTINGS["size"] -= 1
				if event.key == pygame.K_d:
					SETTINGS["size"] += 1
			
				#ENTER KEY PRESSED
				if event.key == pygame.K_RETURN:
					vmf = VMF()
					
					size = SETTINGS["size"]
					disp_size = SETTINGS["increment"] * (2 ** SETTINGS["power"])
					
					y = SETTINGS["y_offset"]
					for each_row in range(size):
						
						x = SETTINGS["x_offset"]
						for each_disp in range(size):
							print("ADDING DISP:" + str(x) + ", " + str(y))
							
							add_displacement(vmf, island, [x, y, 0], [disp_size, disp_size, 16], SETTINGS["increment"])
						
							x += disp_size
							
						y += disp_size
				
					#add_displacement(vmf, island, [-512, -512, 0], [512, 512, 16], 32)
					#add_displacement(vmf, island, [-512, 0, 0], [512, 512, 16], 32)
					#add_displacement(vmf, island, [0, -512, 0], [512, 512, 16], 32)
					#add_displacement(vmf, island, [0, 0, 0], [512, 512, 16], 32)
				
					vmf_file = open("output.vmf", "w")
					vmf_file.truncate()
					write_properties(vmf_file, vmf, 0)
					vmf_file.close()
					
					sys.exit(0)
				
				print(SETTINGS)
				
		#mouse drag
		mouse_pressed = pygame.mouse.get_pressed()
		if mouse_pressed[0]:
			movement = pygame.mouse.get_rel()
			dragging = True
			while(dragging):
				#print("DRAGGINS")
				movement = pygame.mouse.get_rel()
				INFO["x_offset"] += float(movement[0])/INFO["zoom"]
				INFO["y_offset"] += float(movement[1])/INFO["zoom"]
				
				for local_event in pygame.event.get():
					pass
				
				local_mouse_pressed = pygame.mouse.get_pressed()
				if local_mouse_pressed[0] == False:
					dragging = False
					
				island.draw()
				pygame.display.flip()
				
				
		SETTINGS["x_offset"] += SETTINGS["x_velocity"]
		SETTINGS["y_offset"] += SETTINGS["y_velocity"]
				
		island.draw()
		
		INFO["text_pos"] = 0
		add_text("Zoom: " + str(INFO["zoom"]) + "x")
		add_text("1px = " + str(1.0/INFO["zoom"]) + " source units")
		add_text("Size: " + str(SETTINGS["size"]))
		add_text("Power: " + str(SETTINGS["power"]))
		add_text("Increment: " + str(SETTINGS["increment"]))
		add_text("Global Scale: " + str(SETTINGS["global_scale"]))
		add_text("Offset: [" + str(SETTINGS["x_offset"]) + ", " + str(SETTINGS["y_offset"]) + "]")
		
		pygame.display.flip()
			
try:		
	main()
except Exception, ex:
	trace_crash(traceback.print_exc())
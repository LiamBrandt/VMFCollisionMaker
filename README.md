# VMFCollisionMaker
Generates Source Engine displacements by taking terrain in the form of an OBJ file and exporting a Hammer VMF file with displacements similar to that of the given 3D model.

The program will look for 'land.obj' to make the displacement. If your model is not showing up, make sure you take a look at 'config.txt'. The setting "global_scale" will multiply the vertices in the model by that number when importing the model into the program. The default units in the program are Source Engine units, which means 16 units = 1 foot.

Note that the terrain will look flipped in the program, but you can imagine that you are looking from below the model, which will help orient yourself when deciding how to place the grid.

Once you hit 'ENTER' on your keyboard, the displacements will be exported into a Hammer VMF file named 'output.vmf'.

##Requirements:
 * Python 2.7 https://www.python.org/downloads/
 * Pygame http://www.pygame.org/download.shtml

##Usage:
 * Use the arrow keys to move the offset of the displacements around.
 * Use 'A' and 'D' to change the number of displacements used.
 * Use 'W' and 'S' to change distance between each vertice in the displacement.
 * Use 'ENTER' to export the displacements to 'output.vmf'.
 * Use the scroll wheel on your mouse to zoom in and out.
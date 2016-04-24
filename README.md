# VMFCollisionMaker
Generates Source Engine displacements by taking terrain in the form of an OBJ file and exporting a Hammer VMF file with displacements similar to that of the given 3D model.

The program will look for 'land.obj' to make the displacement. If your model is not showing up, make sure you take a look at 'config.txt'. The setting "global_scale" should be how many times bigger your 'land.obj' is from the original LI2 model. So if for example you scaled the original model by 16, then "global_scale" should be 16.

Note that the terrain will look flipped in the program, but you can imagine that you are looking from below the model, which will help orient yourself when deciding how to place the grid.

Once you hit 'ENTER' on your keyboard, the displacements will be exported into a Hammer VMF file named 'output.vmf'.

Usage:
 * Use the arrow keys to move the offset of the displacements around.
 * Use 'A' and 'D' to change the number of displacements used.
 * Use 'W' and 'S' to change distance between each vertice in the displacement.
 * Use 'ENTER' to export the displacements to 'output.vmf'.
 * Use the scroll wheel on your mouse to zoom in and out.
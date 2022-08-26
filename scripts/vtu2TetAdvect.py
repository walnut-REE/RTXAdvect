import os
import numpy as np
import meshio

#Cell-wise solution from GCRS
mesh_fp = "..\dataset\spot\spots.vtk"
out_dir = os.path.dirname(mesh_fp)

mesh = meshio.read(mesh_fp)
n_points, n_cells = len(mesh.points), len(mesh.cells_dict['tetra'])
print("Loading mesh from %s. n_points=%d, n_cells=%d."%(mesh_fp, n_points, n_cells))

print("Converting mesh vertices: ", n_points)
head_line= "NumTetVerts= %d\nx y z" %(n_points)
np.savetxt(os.path.join(out_dir, "verts.dat"), mesh.points, header=head_line, delimiter=" ", fmt="%s",comments="")

print("Converting mesh cells: ", n_cells)
head_line= "NumTetCells= %d\nid1 id2 id3 id4" %(n_cells)
np.savetxt(os.path.join(out_dir, "cells.dat"), mesh.cells_dict['tetra'], header=head_line, delimiter=" ", fmt="%s",comments="")

print("Converting cell attributes: ", mesh.cell_data.keys())
if 'Pressure' in mesh.cell_data.keys() and 'Velocity' in mesh.cell_data.keys():
    head_line= "p u v w"
    PUVW=np.hstack([mesh.cell_data['Pressure'][0].reshape(n_cells,1), mesh.cell_data['Velocity'][0]])
    np.savetxt(os.path.join(out_dir, "solutions_cell.dat"), PUVW, header=head_line, delimiter=" ", fmt="%s",comments="")
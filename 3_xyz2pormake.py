import os
import subprocess
import numpy as np
import pandas as pd
from subprocess import PIPE
from scipy.spatial.distance import euclidean

nodes = [i.split('_')[1].split('.sdf')[0] for i in os.listdir('data/conformers') if 'conformers' in i]

os.makedirs('output_for_pormake',exist_ok=True)

for node in nodes:
    print(f'Now on node: {node}')
    base_dir = f'output/{node}/'
    xyz_H_dir = 'output_for_pormake/xyz_h/'
    xyz_X_dir = 'output_for_pormake/xyz_X/'
    print(f'Adding hydrogens ... ')
    # add Hs
    for file in os.listdir(base_dir):
        if not file.startswith('.') and len(os.listdir(base_dir))>0 :
            try:
                mol_num = file.split('_')[1]
                # generate smile strings
                result = subprocess.run(f'obabel {os.path.join(base_dir,file)} -osmi', shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True).stdout.split()[0]
                # remove square brackets
                result = result.replace('[','').replace(']','')
                if '@' not in result:
                    os.makedirs(os.path.join(xyz_H_dir,node),exist_ok=True)
                    # add hydrogen
                    target_xyz_path = f'output_for_pormake/xyz_h/{node}/mol_{mol_num}.xyz'
                    subprocess.run(f'obabel -:"{result}" --gen3D -O {target_xyz_path}', shell=True)
                    # remove invalid structures
                    info = ''.join(open(target_xyz_path).readlines())
                    if 'nan' in info:
                        os.remove(target_xyz_path)
            except:
                pass

    print(f'Adding connection points ... ')
    # add Xs
    for file in os.listdir(os.path.join(xyz_H_dir,node)):
        if not file.startswith('.'):
                try:
                    data = open(os.path.join(xyz_H_dir,node,file)).readlines() # header = 2
                    lines = [i.strip() for i in data][2:]
                    ele = [i.split()[0] for i in lines]
                    x = [float(i.split()[1]) for i in lines]
                    y = [float(i.split()[2]) for i in lines]
                    z = [float(i.split()[3]) for i in lines]
                    df_xyz = pd.DataFrame({'ele':ele,'x':x,'y':y,'z':z})
                    df_xyz['coord'] = [np.array([x[i],y[i],z[i]]) for i in range(len(df_xyz))]
                    H_xyz = df_xyz[df_xyz.ele=='H']
                    H_indices = list(H_xyz.index)
                    H_coords = list(H_xyz.coord)
                    i_j_pair = []
                    distances = []
                    for i,i_coord in enumerate(H_coords):
                            for j,j_coord in enumerate(H_coords):
                                i_j_pair.append([i,j])
                                distance = euclidean(i_coord,j_coord)
                                distances.append(distance)
                    i_j_pair_max_dist = i_j_pair[distances.index(max(distances))]
                    ind_H1_max_dist = H_indices[i_j_pair_max_dist[0]]
                    ind_H2_max_dist = H_indices[i_j_pair_max_dist[1]]
                    data[ind_H1_max_dist+2] = data[ind_H1_max_dist+2].replace('H','X')
                    data[ind_H2_max_dist+2] = data[ind_H2_max_dist+2].replace('H','X')
                    os.makedirs(os.path.join(xyz_X_dir,node),exist_ok=True)
                    with open(os.path.join(xyz_X_dir,node,'E_'+file),'w+') as f:
                            for line in data:
                                f.write(line)
                except:
                    pass
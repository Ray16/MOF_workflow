from openbabel import pybel
from rdkit import Chem
import os
import subprocess
from subprocess import PIPE

nodes = [i.split('_')[1].split('.sdf')[0] for i in os.listdir('data/conformers') if 'conformers' in i]

os.mkdir('output_for_pormake')

for node in nodes:
    print(f'Now on node: {node}')
    base_dir = f'output/{node}/'
    for file in os.listdir(base_dir):
        if not file.startswith('.'):
            mol_num = file.split('_')[1]
            # generate smile strings
            result = subprocess.run(f'obabel {os.path.join(base_dir,file)} -osmi', shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True).stdout.split()[0]
            # remove square brackets
            result = result.replace('[','').replace(']','')
            os.mkdir(f'output_for_pormake/xyz_h/{node}/')
            os.mkdir(f'output_for_pormake/xyz_X/{node}/')
            # add hydrogen
            target_xyz_path = f'output_for_pormake/xyz_h/{node}/mol_{mol_num}.xyz'
            subprocess.run(f'obabel -:"{result}" --gen3D -O {target_xyz_path}', shell=True)
            # remove invalid structures
            info = ''.join(open(target_xyz_path).readlines())
            if 'nan' in info:
                os.remove(target_xyz_path)


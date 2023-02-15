import os
import sys
import re
import ast
import json
import random
import pathlib
import shutil

from tqdm import tqdm
import timeout_decorator
import pormake as pm

os.makedirs('MOFs',exist_ok=True)

linkers_dir = 'output_for_pormake/xyz_X'
nodes = [i.split('.')[0] for i in os.listdir(linkers_dir)]

database = pm.Database()
#all_tpos = [i.split('.')[0] for i in os.listdir(tpo_dir)]
#all_sbu = [i.split('.')[0] for i in os.listdir(sbu_dir) if not i.startswith('.')]
#all_linkers = sorted([i for i in all_sbu if i.startswith('E')])
#all_nodes = sorted([i for i in all_sbu if not i.startswith('E')])


@timeout_decorator.timeout(5)
def gen_mof(node,linker,tpo):
    T = database.get_topo(tpo)
    N = database.get_bb(node)
    L = database.get_bb(linker)

    builder = pm.Builder()

    node_bbs = {0: N}

    edge_bbs = {(0, 0): L}
    if node+'_'+linker+'.cif' not in os.listdir(mof_dir):
            MOF = builder.build_by_type(topology=T, node_bbs=node_bbs, edge_bbs = edge_bbs)
            cif_name = tpo+'_'+node+'_'+linker+'.cif'
            MOF.write_cif(mof_dir+cif_name)

if __name__ == '__main__':
    os.makedirs('MOFs',exist_ok=True)
    node_dir = 'node_xyz'

    for node in nodes:
        print(f'Now generating MOFs for node: {node}')
        target_mof_dir = os.path.join('MOFs',node)
        mof_dir = f'MOFs/{node}/gen_mofs'

        # copy template PORMAKE dir
        shutil.copytree('PORMAKE_template',target_mof_dir,dirs_exist_ok=True)
        # copy node to bbs dir
        shutil.copy(os.path.join(node_dir,node+'.xyz'),os.path.join(target_mof_dir,'pormake','database','bbs'))
        # copy linkers to bbs dir
        for linker in os.listdir(linkers_dir,node):
            print(f'linker: {linker}')
            shutil.copy(os.path.join(linkers_dir,node,linker),os.path.join(target_mof_dir,'pormake','database','bbs'))
            # generate MOF
            gen_mof(node,linker,'pcu')
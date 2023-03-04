import os
import sys
import shutil
import importlib
from tqdm import tqdm

import timeout_decorator

for n_atoms in range(5,10):
    print(f'Now on n_atoms: {n_atoms}')
    linkers_dir = f'output_for_pormake/n_atoms_{n_atoms}/xyz_X'
    nodes = [i.split('.')[0] for i in os.listdir(linkers_dir)]
    parent_dir = os.path.dirname(os.path.realpath(__file__))


    @timeout_decorator.timeout(5)
    def gen_mof(node,linker,tpo):

        builder = pm.Builder()
        database = pm.Database()

        T = database.get_topo(tpo)
        N = database.get_bb(node)
        L = database.get_bb(linker)

        node_bbs = {0: N}

        edge_bbs = {(0, 0): L}
        if node+'_'+linker+'.cif' not in os.listdir(mof_dir):
                MOF = builder.build_by_type(topology=T, node_bbs=node_bbs, edge_bbs=edge_bbs)
                cif_name = tpo+'_'+node+'_'+linker+'.cif'
                print(f'Generated {cif_name}')
                MOF.write_cif(os.path.join(mof_dir,cif_name))
        

    if __name__ == '__main__':
        os.makedirs('MOFs',exist_ok=True)
        node_dir = 'node_xyz'

        # append pormake path to sys
        sys.path.append('PORMAKE_template')
        print('Loading PORMAKE ...')
        import pormake as pm
        print('PORMAKE loaded ...')

        for node in nodes:
            if node != 'V':
                print(f'Now generating MOFs with node: {node}')
                pormake_dir = 'PORMAKE_template'
                target_mof_dir = os.path.join('MOFs',node)
                mof_dir = f'MOFs/n_atoms_{n_atoms}/{node}/'
                os.makedirs(mof_dir,exist_ok=True)

                # copy node to template pormake bbs dir
                print(f'cp node {node} to pormake dir ...')
                shutil.copy(os.path.join(node_dir,node+'.xyz'),os.path.join(pormake_dir,'pormake','database','bbs'))

                # copy linkers to template poramke bbs dir
                print('cp linkers to pormake dir ...')
                for linker in os.listdir(os.path.join(linkers_dir,node)):
                    shutil.copy(os.path.join(linkers_dir,node,linker),os.path.join(pormake_dir,'pormake','database','bbs'))

                # generate MOF
                linker_names = [i.split('.')[0] for i in os.listdir(os.path.join(linkers_dir,node)) if 'E_' in i]
                for l in tqdm(linker_names):
                    gen_mof(node,l,'pcu')

                # remove sbus from PORMAKE template folder
                shutil.rmtree(os.path.join(pormake_dir,'pormake','database','bbs'))
                os.mkdir(os.path.join(pormake_dir,'pormake','database','bbs'))
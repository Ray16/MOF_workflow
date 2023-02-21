import os
import sys
import shutil
import importlib
from tqdm import tqdm

import timeout_decorator


os.makedirs('MOFs',exist_ok=True)

linkers_dir = 'output_for_pormake/xyz_X'
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
    print('Finished loading PORMAKE ...')

    for node in nodes:
        if node != 'V':
            print(f'Now generating MOFs with node: {node}')
            pormake_dir = 'PORMAKE_template'
            target_mof_dir = os.path.join('MOFs',node)
            mof_dir = f'MOFs/{node}/'
            os.makedirs(mof_dir,exist_ok=True)

            # copy template PORMAKE code to MOFs dir
            #shutil.copytree('PORMAKE_template',target_mof_dir,dirs_exist_ok=True)

            # copy node to template pormake bbs dir
            print(f'Copying node {node} to pormake dir ...')
            shutil.copy(os.path.join(node_dir,node+'.xyz'),os.path.join(pormake_dir,'pormake','database','bbs'))

            # copy linkers to template poramke bbs dir
            print('Copying linkers to pormake dir ...')
            for linker in os.listdir(os.path.join(linkers_dir,node)):
                shutil.copy(os.path.join(linkers_dir,node,linker),os.path.join(pormake_dir,'pormake','database','bbs'))

            # append pormake path
            #sys.path.append(os.path.join('MOFs',node)) # append pormake path to sys
            #os.chdir(os.path.join(parent_dir,'MOFs',node))

            # generate MOF
            linker_names = [i.split('.')[0] for i in os.listdir(os.path.join(linkers_dir,node)) if 'E_' in i]
            for l in tqdm(linker_names):
                gen_mof(node,l,'pcu')
                break
            
            # move generated MOFs to the target dir
            #for MOF in os.path.join():
            #    shutil.move('',)

            # remove sbus from PORMAKE template folder
            shutil.rmtree(os.path.join(pormake_dir,'pormake','database','bbs'))
            os.mkdir(os.path.join(pormake_dir,'pormake','database','bbs'))

            #del pm
            #os.chdir(parent_dir)
            # remove completed pormake job path from sys path
            #sys.path.remove(os.path.join('MOFs',node))
            #sys.modules.pop('pormake')
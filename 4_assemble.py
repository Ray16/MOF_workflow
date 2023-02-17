import os
import sys
import shutil
from tqdm import tqdm

import timeout_decorator


os.makedirs('MOFs',exist_ok=True)

linkers_dir = 'output_for_pormake/xyz_X'
nodes = [i.split('.')[0] for i in os.listdir(linkers_dir)]

@timeout_decorator.timeout(5)
def gen_mof(node,linker,tpo):
    import pormake as pm
    print(pm.__file__)
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

    for node in nodes:
        if node != 'V':
            print(f'Now generating MOFs with node: {node}')
            target_mof_dir = os.path.join('MOFs',node)
            mof_dir = f'MOFs/{node}/gen_mofs'

            # copy template PORMAKE code to MOFs dir
            shutil.copytree('PORMAKE_template',target_mof_dir,dirs_exist_ok=True)
            sys.path.append(os.path.join('MOFs',node)) # append pormake path to sys
            print(sys.path)
            import pormake as pm

            # copy node to bbs dir
            print(f'Copying node {node} to pormake dir ...')
            shutil.copy(os.path.join(node_dir,node+'.xyz'),os.path.join(target_mof_dir,'pormake','database','bbs'))

            # copy linkers to bbs dir
            print('Copying linkers to pormake dir ...')
            for linker in os.listdir(os.path.join(linkers_dir,node)):
                shutil.copy(os.path.join(linkers_dir,node,linker),os.path.join(target_mof_dir,'pormake','database','bbs'))
            
            # generate MOF
            linker_names = [i.split('.')[0] for i in os.listdir(os.path.join(linkers_dir,node)) if 'E_' in i]
            for l in tqdm(linker_names):
                gen_mof(node,l,'pcu')
                break

            # remove the previous pormake path
            print(sys.path)
            sys.path.remove(os.path.join('MOFs',node))
            print(sys.path)
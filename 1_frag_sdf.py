import os
from glob import glob
import shutil
import subprocess

nodes = [i.split('_')[1].split('.sdf')[0] for i in os.listdir('data/conformers') if 'conformers' in i]

for node in nodes:
    print(f'Now on node {node}')
    TARGET_DIR = f'data/sdf/{node}/'
    INPUT_SMILES=f'data/fragments_smi/frag_{node}_unique.txt'
    OUTPUT_TEMPLATE='hMOF'
    OUT_DIR=f'data/fragments_all/{node}/'
    CORES='32'
    
    # generate sdf of molecular fragments
    os.makedirs(TARGET_DIR,exist_ok=True)
    subprocess.run(['python','-W','ignore','rdkit_conf_parallel.py',INPUT_SMILES,OUTPUT_TEMPLATE,'--cores',CORES],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for sdf in glob('*.sdf'):
        shutil.move(sdf,TARGET_DIR) 
    
    # generate sdf for frags and linkers
    os.makedirs(OUT_DIR,exist_ok=True)
    subprocess.run(f'python -W ignore prepare_dataset_parallel.py --table {INPUT_SMILES} --sdf-dir {TARGET_DIR} --out-dir {OUT_DIR} --template {OUTPUT_TEMPLATE} --cores {CORES}',shell=True)

    # filter and merge fragments
    subprocess.run(f'python -W ignore filter_and_merge.py --in-dir {OUT_DIR} --out-dir {OUT_DIR} --template {OUTPUT_TEMPLATE} --number-of-files {CORES}',shell=True)
    
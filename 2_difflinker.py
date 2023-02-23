import os
import argparse
import subprocess
import multiprocessing

parser = argparse.ArgumentParser()
parser.add_argument('--n_atoms', action='store', type=int, required=True, help='number of atoms to sample')
args = parser.parse_args()

nodes = [i.split('_')[1].split('.sdf')[0] for i in os.listdir('data/conformers') if 'conformers' in i]

n_atoms = args.n_atoms
print(f'Sampling {n_atoms} atoms ...')
for node in nodes:
    print(f'Now on node: {node}')
    OUTPUT_DIR = f'output/n_atoms_{n_atoms}/{node}'
    os.makedirs(OUTPUT_DIR,exist_ok=True)
    subprocess.run(f'python -W ignore utils/difflinker_sample_and_analyze.py --linker_size {n_atoms} --fragments data/fragments_all/{node}/hMOF_frag.sdf --model models/geom_difflinker.ckpt --output {OUTPUT_DIR} --n_samples 1',shell=True)
    #subprocess.run(f'python -W ignore utils/difflinker_sample_and_analyze.py --linker_size models/geom_size_gnn.ckpt --fragments data/fragments_all/{node}/hMOF_frag.sdf --model models/geom_difflinker.ckpt --output {OUTPUT_DIR} --n_samples 1',shell=True) 
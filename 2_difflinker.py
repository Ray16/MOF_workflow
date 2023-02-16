import os
import subprocess
import multiprocessing

nodes = [i.split('_')[1].split('.sdf')[0] for i in os.listdir('data/conformers') if 'conformers' in i]

os.makedirs('output',exist_ok=True)

for node in nodes:
    print(f'Now on node: {node}')
    OUTPUT_DIR = f'output/{node}'
    os.makedirs(OUTPUT_DIR,exist_ok=True)
    subprocess.run(f'python -W ignore utils/difflinker_sample_and_analyze.py --linker_size 6 --fragments data/fragments_all/{node}/hMOF_frag.sdf --model models/geom_difflinker.ckpt --output {OUTPUT_DIR} --n_samples 1',shell=True)
    #subprocess.run(f'python -W ignore utils/difflinker_sample_and_analyze.py --linker_size models/geom_size_gnn.ckpt --fragments data/fragments_all/{node}/hMOF_frag.sdf --model models/geom_difflinker.ckpt --output {OUTPUT_DIR} --n_samples 1',shell=True) 
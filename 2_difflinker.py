import os
from tqdm import tqdm
import subprocess

nodes = [i.split('_')[1].split('.sdf')[0] for i in os.listdir('data') if 'conformers' in i]

for node in tqdm(nodes):
    OUTPUT_DIR = f'output/{node}'
    os.mkdir(OUTPUT_DIR)
    subprocess.run(f'python -W ignore difflinker_sample_and_analyze.py --fragments data/fragments_all/{node}/hMOF_frag.sdf --model models/geom_difflinker.ckpt --linker_size models/geom_size_gnn.ckpt --output {OUTPUT_DIR} --n_samples 1')
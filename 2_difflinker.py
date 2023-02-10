import os
from subprocess import run

nodes = [i.split('_')[1].split('.sdf')[0] for i in os.listdir('data') if 'conformers' in i]

for node in nodes:
    OUTPUT_SAMPLE_DIR = f'output_samples/{node}'
    os.mkdir(OUTPUT_SAMPLE_DIR)
    run(['python','-W','ignore','difflinker_sample_and_analyze.py','--fragments',f'data/fragments_all/{node}/hMOF_frag.sdf','--model','models/geom_difflinker.ckpt','--linker_size','models/geom_size_gnn.ckpt','--output','output','--samples_dir',OUTPUT_SAMPLE_DIR,'--n_samples','1'])
    break
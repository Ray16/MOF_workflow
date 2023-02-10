import os
from subprocess import run

nodes = [i.split('_')[1].split('.sdf')[0] for i in os.listdir('data') if 'conformers' in i]

for node in nodes:
    run(['python','-W','ignore','difflinker_sample_and_analyze.py','--fragments',f'data/fragments_all/{node}/hMOF_frag.sdf','--model','models/geom_difflinker.ckpt','--linker_size','models/geom_size_gnn.ckpt','--output','output','--samples_dir','output_samples','--n_samples','1'])
    break
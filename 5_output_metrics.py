import os
import pandas as pd
from rdkit import Chem
import subprocess

true_base_dir = 'data/fragments_all/'
pred_base_dir = 'output/'

os.makedirs('metrics',exist_ok=True)
for sys in os.listdir(pred_base_dir):
    if 'smiles' not in sys:
        true_smiles_all = []
        frag_smiles_all = []
        pred_smiles_all = []
        for i,linker in enumerate(os.listdir(os.path.join(pred_base_dir,sys))):
            # generate for SMILES_true
            line = pd.read_csv(os.path.join(true_base_dir,sys,'hMOF_table.csv')).iloc[i,:]
            true_smiles_all.append(line[1].strip())
            # generate for SMILES_frag
            frag_smiles_all.append(line[2].strip())
            # generate for SMILES_pred
            pred_smiles_all.append(open(os.path.join(pred_base_dir,'smiles_'+sys+'.csv')).readlines()[i])
        df = pd.DataFrame({'index':range(len(true_smiles_all)),'true_molecules':true_smiles_all,'pred_molecules':pred_smiles_all,'frag_molecules':frag_smiles_all})
        df = df[~df["pred_molecules"].str.contains('@')] # remove bad entries
        df.to_csv(f'metrics/{sys}.csv',index=False)
    subprocess.run([f'python -m evaluation.linkers --save_result --filename metrics/{sys}.csv'])
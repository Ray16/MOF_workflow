import os
import pandas as pd
from rdkit import Chem

true_base_dir = 'data/fragments_all/'
pred_base_dir = 'output_for_pormake/xyz_h/'

os.makedirs('metrics',exist_ok=True)
for sys in os.listdir(pred_base_dir):
    true_smiles_all = []
    frag_smiles_all = []
    pred_smiles_all = []
    for i,linker in enumerate(os.listdir(os.path.join(pred_base_dir,sys))):
        # generate for SMILES_true
        line = pd.read_csv(os.path.join(pred_base_dir,sys,'hMOF_table.csv')).iloc[i,:]
        true_smiles_all.append(line[1])
        # generate for SMILES_frag
        frag_smiles_all.append(line[2])
        # generate for SMILES_pred
        pred_mol = Chem.MolFromXYZBlock(os.path.join(pred_base_dir,sys,linker))
        pred_smiles_all.append(Chem.MolToSMILES(pred_mol))
    print(true_smiles_all)
    print(frag_smiles_all)
    print(pred_smiles_all)

import os
import ast
import subprocess
import itertools
from tqdm import tqdm
import numpy as np
import pandas as pd
import seaborn as sns
import rdkit.Chem.AllChem as Chem
from rdkit.Chem import AllChem
import matplotlib.pyplot as plt

# data cleaning
df_info = pd.read_csv('data/hMOF_CO2_info.csv')
df_info = df_info.dropna() # drop entries containing 'NaN'
df_info = df_info[df_info.CO2_wc_001>0] # only keep entries with positive CO2 working capacity
df_info = df_info[~df_info.MOFid.str.contains('ERROR')] # drop entries with error
df_info = df_info[~df_info.MOFid.str.contains('NA')] # drop entries with NA

# get node and linker information
metal_eles = ['Zn', 'Cu', 'Mn', 'Zr', 'Co', 'Ni', 'Fe', 'Cd', 'Pb', 'Al', 'Mg', 'V',
       'Tb', 'Eu', 'Sm', 'Tm', 'Gd', 'Nd', 'Dy', 'La', 'Ba', 'Ga', 'In',
       'Ti', 'Be', 'Ce', 'Li', 'Pd', 'Na', 'Er', 'Ho', 'Yb', 'Ag', 'Pr',
       'Cs', 'Mo', 'Lu', 'Ca', 'Pt', 'Ge', 'Sc', 'Hf', 'Cr', 'Bi', 'Rh',
       'Sn', 'Ir', 'Nb', 'Ru', 'Th', 'As', 'Sr']

# get a list of metal nodes & create a new column named "metal_nodes"
metal_nodes = []
organic_linkers = []
for i,mofid in tqdm(enumerate(df_info.MOFid)):
    sbus = mofid.split()[0].split('.')
    metal_nodes.append([c for c in sbus if any(e in c for e in metal_eles)][0])
    organic_linkers.append([c for c in sbus if any(e in c for e in metal_eles)==False])

df_info['metal_node'] = metal_nodes
df_info['organic_linker'] = organic_linkers

# get most occuring nodes
unique_nodes = [n for n in list(df_info['metal_node'].unique()) if len(n)<=30] # node smiles should be shorter then 30 strings
df_info = df_info[df_info['metal_node'].isin(unique_nodes)] # filter df_info based on unique_nodes
freq = [df_info['metal_node'].value_counts()[value] for value in list(df_info.metal_node.unique())] # get frequency of unique nodes
df_freq = pd.DataFrame({'node':list(df_info.metal_node.unique()),'freq':freq})
print('node occurance:')
print(df_freq)
unique_node_select = list(df_freq[df_freq.freq>=5000].node) # select occuring nodes
df_info_select = df_info[df_info['metal_node'].isin(unique_node_select)] # select df_info with node only in list(unique_node_select)

# output each node to a separate csv files
for n in unique_node_select:
    df_info_select_node = df_info[df_info.metal_node == n]
    df_info_select_node.to_csv(f'data/data_by_node/{n}.csv',index=False)

# load data
for node in unique_node_select:
    print(f'Now on node {node} ... ')
    input_data_path = f'data/data_by_node/{node}.csv' 
    output_data_path = f'data/data_high_wc/{node}.csv'

    df = pd.read_csv(input_data_path)

    # select entries with high working capactiy at (wc > 2mmol/g @ 0.1 bar)
    df_high_wc = df[df['CO2_wc_01'] >=2]

    # select entries with three parsed linkers
    len_linkers = [len(ast.literal_eval(df_high_wc['organic_linker'].iloc[i])) for i in range(len(df_high_wc['organic_linker']))]
    df_high_wc['len_linkers'] = len_linkers
    df_high_wc_select = df_high_wc[df_high_wc.len_linkers==3]
    df_high_wc_select.to_csv(output_data_path,index=False)

    # get list of SMILES for all linkers
    list_smiles = [ast.literal_eval(i) for i in df_high_wc_select['organic_linker']]
    all_smiles = list(itertools.chain(*list_smiles))

    # output to sdf
    print('Outputting conformers to sdf ... ')
    os.makedirs(f'data/conformers',exist_ok=True)
    conformer_sdf_path = f'data/conformers/conformers_{node}.sdf'

    writer = Chem.SDWriter(conformer_sdf_path)
    for smile in tqdm(all_smiles):
        try:
            mol = Chem.AddHs(Chem.MolFromSmiles(smile))
            conformers = AllChem.EmbedMultipleConfs(mol, numConfs=1)
            conformer = mol.GetConformer(0)
            for cid in range(mol.GetNumConformers()):
                writer.write(mol, confId=cid)
        except:
            pass
    
    # generate SMILES
    print('Generating SMILES ... ')
    subprocess.run(f'python prepare_data_from_sdf.py --sdf_path data/conformers/conformers_{node}.sdf --output_path data/fragments_smi/frag_{node}.txt --verbose',shell=True)

    # remove duplicates
    data = open(f'data/fragments_smi/frag_{node}.txt').readlines()
    #print(f'# of fragment-linker pairs: {len(data)}')
    unique_data = pd.Series(data).unique()
    #print(f'# of unique fragment-linker pairs: {len(unique_data)}')
    with open(f'data/fragments_smi/frag_{node}_unique.txt','w+') as f:
        for line in unique_data:
            f.write(line)

## Diffusion model accelerates computational deisng of MOF structures for CO2 capture

This framework enables generation of new MOFs structures with desinated node/topology and DiffLinker-generated linkers, which are derived from parsed linkers from high-performing MOFs in the hMOF database.

The following steps are used for new linker generation:
1. Select high-performing MOFs from hMOF database based on CO2 working capacity
2. Parse the SMILES strings of MOF linkers based on MOFid
3. Use Matched Molecular Pair Algorithm (MMPA) to fragment linkers into components
4. Use DiffLinker to generate new linkers
5. Use PORMAKE to assemble the newly generated linkers with desinated node/topology into MOFs

The following files were borrowed from DeLinker (in the *utils* dir):
- prepare_data_from_sdf.py
- fpscores.pkl.gz
- frag_utils.gz
- sascorer.py
- wehi_pains.csv

The following files were borrowed from DiffLinker (in the *utils* dir):
- filter_and_merge.py
- prepare_dataset.py
- prepare_dataset_parallel.py
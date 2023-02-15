Iterative design of MOF structures using generative models

This framework is based on DeLinker and DiffLinker, which enables generation of new organic linkers with parsed linkers from high-performing MOFs from the hMOF database. The default target property is 2 mmol/g @ 0.1 bar.

The following steps:
1. Select high-performing MOFs from hMOF database based on CO2 working capacity
2. Parse the SMILES strings of organic linkers based on MOFid
3. Use Matched Molecular Pair Algorithm (MMPA) to fragment linkers into their components
4. Use DiffLinker to generate new linkers
5. Use PORMAKE to assemble the newly generated linkers into MOFs

The following files were taken from DeLinker:
- prepare_data_from_sdf.py
- fpscores.pkl.gz
- frag_utils.gz
- sascorer.py
- wehi_pains.csv

The following files were taken from DiffLinker:

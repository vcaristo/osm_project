1) Modify python script to count features of single state, passed as an argument
- See `count_features_apptainer-Parallel-Nodes.py`

2) Create a list of all the states

```bash
ls ~/osm_project/data > ~/osm_project/data/states.txt
```

3) Create a SLURM array script

- see `count_features_batch-Parallel-Nodes.sh`

4) Combine the results from each node
- see `count_features.ipynb'
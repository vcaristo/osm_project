#!/bin/bash
#SBATCH --job-name=count-features
#SBATCH --output=slurm_out/count-features_49_machines.out
#SBATCH --error=slurm_out/count-features_49_machines.err
#SBATCH --time=12:00:00
#SBATCH --array=0-49
#SBATCH --mem=16G
#SBATCH --cpus-per-task=1
#SBATCH --mail-type=all
#SBATCH --mail-user=vc149353@umconnect.umt.edu

# There are three path parameters after 'apptainer run'

# 1. --bind <path_to_local_folder>:<path_in_apptainer>' 
#   This mounts your local folder at <path_to_local_folder> into the apptainer at <path_in_apptainer>
#   You can think of this as a direct mapping 
# 2. <path to the apptainer sif>
# 3. <path to the script to run> 
#   Note, this is the script's path inside the apptainer (using <apptainer_path>)

# 'apptainer run --bind <path_to_local_folder>:<path_in_apptainer> <path to the apptainer sif> <path to the script to run>'


#START=$(date +%s)

mapfile -t STATES < ~/osm_project/data/states.txt

STATE=${STATES[$SLURM_ARRAY_TASK_ID]}

apptainer run --bind ~/osm_project/:/mnt/osm_project/ \
        ~/osm_project/hpc/apptainer/geopy_container.sif \
        /mnt/osm_project/dev/count_features/count_features_apptainer_Parallel-Nodes.py "$STATE"

#END=$(date +%s)
#RUNTIME=$((END - START))


#echo "Run time: $RUNTIME seconds ($(awk "BEGIN {print $RUNTIME/60}") minutes)"
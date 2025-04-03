#!/bin/bash
#SBATCH --job-name=osm-download
#SBATCH --output=osm-download.out
#SBATCH --error=osm-download.err
#SBATCH --time=12:00:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=1
#SBATCH --mail-type=all
#SBATCH --mail-user=vc149353@umconnect.umt.edu

# Load conda and activate environment
module load conda

# init conda
$(conda info --base)/etc/profile.d/conda.sh

conda activate us_osm_env

# Run the script
python download_osm_features.py
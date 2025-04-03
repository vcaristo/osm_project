#!/bin/bash
#SBATCH --job-name=osm-download
#SBATCH --output=osm-download.out
#SBATCH --error=osm-download.err
#SBATCH --time=12:00:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=1

# Load conda and activate environment
module load conda
conda activate ox

# Run the script
python download_osm_features.py
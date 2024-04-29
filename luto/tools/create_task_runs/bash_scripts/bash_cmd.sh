#!/bin/bash

# Read the settings_bash file
source luto/settings_bash.py


# Set the memory and time based on the resolution factor
if [ "$RESFACTOR" -eq 1 ]; then
    MEM="200G"
    TIME="30-0:00:00"
elif [ "$RESFACTOR" -eq 2 ]; then
    MEM="150G"
    TIME="10-0:00:00"
elif [ "$RESFACTOR" -eq 3 ]; then
    MEM="100G"
    TIME="5-0:00:00"
else
    MEM="80G"
    TIME="2-0:00:00"
fi



# Get the job name based on the task directory
SCRIPT_PATH=$(realpath $(dirname "$0"))
PARENT_DIR=$(basename "${SCRIPT_PATH}")
JOB_NAME="LUTO_${PARENT_DIR}"




#SBATCH -p mem                      	# Partition name
#SBATCH --time=${TIME}            	    # Runtime in D-HH:MM:SS
#SBATCH --mem=${MEM}                	# Memory total in GB
#SBATCH --cpus-per-task=32          	# Number of CPUs per task
#SBATCH --job-name=${JOB_NAME}          # Job name





# Activate the Conda environment
source ~/miniconda3/etc/profile.d/conda.sh
source ~/miniforge3/etc/profile.d/conda.sh
source ~/anaconda3/etc/profile.d/conda.sh
conda activate luto


# Run the simulation
python <<-EOF
import luto.simulation as sim
data = sim.load_data()
sim.run(data=data, base=2010, target=2050)
from luto.tools.write import write_outputs
write_outputs(data)
EOF
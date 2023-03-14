FROM gitpod/workspace-full:latest

USER root

RUN sudo apt-get update && \
    sudo apt-get install -y rsync && \
    apt-get install -y procps 

#install snakemake and dependencies
RUN curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh -o Mambaforge-Linux-x86_64.sh && \
echo "yes" | bash Mambaforge-Linux-x86_64.sh

#create conda env and dependencies for snakemake
RUN conda activate base
RUN mamba env create --name annotate -f environment.yaml && \
    conda activate annotate &&\
    cpanm Compress::Raw::Zlib

#setup api

# Copy the current directory contents into the container at /api except large data files
#COPY . /api --exclude data/
#COPY . /api

# Set the working directory to /api
WORKDIR /api

# Expose the API port
EXPOSE 5000

# Run the command to start the API
CMD [ "python", "api.py" ]
# Give back control
USER root
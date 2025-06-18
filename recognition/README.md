# Recognition

## First-Time Setup

### Installing 
- Run `recognition/install.sh` to set up a docker container that serves as a starting point for the pre-made python scripts

### Installing for development
- Run `recognition/install_dev.sh` to install the python environment locally

## Training

### Start Training
- ``recognition/run.sh train tsr_example``
- or without docker: ``cd recognition && python entrypoint.py train tsr_example``

and to resume training:
- ``recognition/run.sh train tsr_example --resume``


### Visualization & Logging
Start TensorBoard:  
- ``tensorboard --logdir runs/yolo_custom_training``
- ``tensorboard --logdir .\runs\train\experiment_20250618_205355\``

Open in browser: 
- http://localhost:6006/

## Inference

### Start Inference
- ``recognition/run.sh inference tsr_example``

# Deepdub CLI - Installation Guide
Deepdub has been (successfully) tested on a Linux environment with the following specs:
- Ubuntu 20.04.3 LTS
- 64-bit
- 16GB DDR4 memory
- AMD® Ryzen 5 3600 6-core processor × 12
- NVIDIA Corporation GP104 [GeForce GTX 1070]


Here are the steps to get it up and running on a similar system.

## Step 1: Virtual Environment
Create a virtual environment with Python version 3.7. 
You can use:
- conda, or 
- virtualenv 
to achieve this.

## Step 2a: Low-level libraries (FFMpeg)
Install ```ffmpeg``` using apt (Ubuntu) or compile from source or download the executable (Windows).

## (if using Ubuntu) Step 2b: System libraries
It's possible that you may not have the essential libraries to run a low-level Python project.
Here are some commands which can "fill in" the empty gaps you might have.

```
sudo apt-get install build-essential libssl-dev libffi-dev
sudo apt-get install libxml2-dev libxslt1-dev zlib1g-dev 
sudo apt-get install python3-pip
sudo apt-get install python3 python-dev python3-dev
sudo apt-get install libportaudio2
```

You can install all such dependencies (which we know of) using the following command, assuming you're in the **deepdub_cli** folder:
```
bash install_dependencies.sh
```

## Step 3: Installing Pytorch for Real-Time-Voice-Cloning
Install Pytorch by looking up the proper syntax [here](https://pytorch.org/get-started/locally/)

Just some examples:
- pip:
```
pip3 install torch torchvision torchaudio
```

- conda:
```
conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch
```

## Step 4: Models
Download the pretrained models for each module.

- Real-Time-Voice-Cloning: https://github.com/CorentinJ/Real-Time-Voice-Cloning/wiki/Pretrained-models
- Face Detection, Wav2Lip: https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth
- Weights, Wav2Lip: https://iiitaphyd-my.sharepoint.com/personal/radrabha_m_research_iiit_ac_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fradrabha%5Fm%5Fresearch%5Fiiit%5Fac%5Fin%2FDocuments%2FWav2Lip%5FModels%2Fwav2lip%2Epth&parent=%2Fpersonal%2Fradrabha%5Fm%5Fresearch%5Fiiit%5Fac%5Fin%2FDocuments%2FWav2Lip%5FModels


More info (e.g. where to place the files, any alt links etc) is at the repos of each module.

RTVC: https://github.com/CorentinJ/Real-Time-Voice-Cloning 
W2L:  https://github.com/Rudrabha/Wav2Lip


## Step 5: It's all coming together.
By now you probably got that this current pipeline is simply putting two modules together into one serial flow. So each module has its own installation procedure and magically (a.k.a. luckily) their installations do not conflict with each other. So we've made one requirements.txt file which contains the requirements of both these modules, called ```requirements_deepdub-cli_37.txt```. 

You can install the requirements from this file using:
```
pip install -r requirements_deepdub-cli_37.txt
```


## Step 6: Done! Now let's run it...
Here's a sample run of the deepdub CLI.
```
python main.py -vd /home/saad/Projects/FYP/squidgames/ep1.mp4 -tn /home/saad/Projects/FYP/squidgames/subtitles/ep1.srt -dds 00:14:00 -dde 00:14:23 -cml 1.5 -e encoder/saved_models/pretrained.pt -s synthesizer/saved_models/pretrained/pretrained.pt -v vocoder/saved_models/pretrained/pretrained.pt --checkpoint_path /home/saad/Projects/deepdub/deepdub-cli/checkpoints/wav2lip.pth --outfile results/result_voice.mp4 --fps 25.0 --pads 0 10 0 0 --face_det_batch_size 16 --wav2lip_batch_size 128 --resize_factor 1 --crop 0 -1 0 -1 --box -1 -1 -1 -1
```

As you can see, that's a lot to absorb. Luckily you don't have to give all the options, just some are enough. You can run the following command for more help.
```python main2.py --help```



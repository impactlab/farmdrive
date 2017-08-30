# End-to-end AWS EC2 setup, data download, and model training

US West (Oregon) Region
UBUNTU 16.04 AMI
g2.2xlarge
Add EBS volume (1000 GB)

## Install updates for machine
Update defaults

```
sudo apt-get update
sudo apt-get -y dist-upgrade
```

## Install OSSIM

```
sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
sudo apt-get update
sudo apt-get install ossim-core
```

## Make sure EBS is mounted
http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html
```
lsblk
sudo file -s /dev/<EBS_DEVICE>
sudo mkfs -t ext4 /dev/<EBS_DEVICE>
sudo mkdir /dd
ls -al /dev/disk/by-uuid/

In /etc/fstab add the line:
UUID=<UUID_OF_DISK_FROM_LS>       /dd   ext4    defaults,nofail        0       2

sudo mount -a
sudo chown ubuntu /dd
```

## Install NVIDIA Drivers

Add nvidia driver repo
```
sudo add-apt-repository ppa:graphics-drivers/ppa
```

Find the latest _recommended_ driver using this tool:
http://www.nvidia.com/Download/Find.aspx
```
G2 Instances

Product Type	GRID
Product Series	GRID Series
Product	GRID K520
Operating System	Linux 64-bit
Recommended/Beta	Recommended/Certified
```

Install that driver (e.g., nvidia-367)
```
sudo apt-get install nvidia-<MAJOR_VERSION_NUMBER>
```

## Install CUDA
https://developer.nvidia.com/cuda-downloads
Linux
x86_64
Ubuntu
16.04
runfile (local)

```
wget https://developer.nvidia.com/compute/cuda/8.0/prod/local_installers/cuda_8.0.44_linux-run
sudo sh cuda_8.0.44_linux-run
```
Responses:
 - accept
 - Install NVIDIA Accelerated Graphics Driver for Linux-x86_64 367.48?
  - n (already did it)
- Install the CUDA 8.0 Toolkit?
  - y
- Enter Toolkit Location
  - /dd/lib/cuda-8.0 (to make sure we have enough space ~4.5GB)

```sudo nano ~/.bashrc```

Add these lines:

```
  export PATH=$PATH:/dd/lib/cuda-8.0/bin
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/dd/lib/cuda-8.0/lib64
```

```
source ~/.bashrc
```


## Install cuDNN
https://developer.nvidia.com/rdp/cudnn-download
Download cuDNN v5.1 (August 10, 2016), for CUDA 8.0
cuDNN v5.1 Library for Linux

On local machine (where you can download the file in a browser)
```
scp -i permissions <PATH_TO cudnn-8.0-linux-x64-v5.1-ga.tgz> ubuntu@<AWS EC2 MACHINE IP>:/dd/machine_setup
```

```
tar -zxf cudnn-8.0-linux-x64-v5.1-ga.tgz
cp cuda/lib64/* /dd/lib/cuda-8.0/lib64/
cp cuda/include/* /dd/lib/cuda-8.0/include/
```

## Install Anaconda
https://www.continuum.io/downloads
```
wget https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh
```

Change the location to the EBS volume!!
```
Anaconda3 will now be installed into this location:
/home/ubuntu/anaconda3

  - Press ENTER to confirm the location
  - Press CTRL-C to abort the installation
  - Or specify a different location below

[/home/ubuntu/anaconda3] >>> /dd/anaconda3

...

Do you wish the installer to prepend the Anaconda3 install location
to PATH in your /home/ubuntu/.bashrc ? [yes|no]
[no] >>> yes

```

Run

```
source ~/.bashrc
```

## clone git repo
```
git clone git@github.com:impactlab/farmdrive.git
```

## Install Postgres + PostGIS

```
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib
sudo apt-get install -y postgis postgresql-9.5-postgis-2.2
sudo -u postgres createuser --interactive
 - ubuntu
 - y
make create_db
```

psycopg2 expects socket at /tmp

```
sudo nano /etc/postgresql/9.5/main/postgresql.conf

unix_socket_directories = '/tmp,/var/run/postgresql'    # comma-separated list of directories
```

```
sudo service postgresql restart
```


## install R (for r2py)
```
sudo apt-get install r-base
```

## Normal env setup
```
make new_env
source activate farmdrive
```

## Install tensorflow

# Ubuntu/Linux 64-bit, GPU enabled, Python 3.5
# Requires CUDA toolkit 8.0 and CuDNN v5.1. For other versions, see "Installing from sources" below.

```
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-0.12.1-cp35-cp35m-linux_x86_64.whl
pip install --upgrade $TF_BINARY_URL
```


https://www.tensorflow.org/get_started/os_setup

## Install Keras
```
conda install h5py numpy scipy
pip install keras
python -c 'import keras'
```

import line ensures we create the configuration file ~/.keras/keras.json

```
nano ~/.keras/keras.json
```

```
{
    "floatx": "float32",
    "backend": "tensorflow",
    "image_dim_ordering": "tf",
    "epsilon": 1e-07
}
```

# restart to make sure everything gets loaded
```
reboot
```

## Download the data folder
Enter just the access key and secret access key
```
aws configure
```

make sync_data_from_s3

make data

## Download the planet scenes
Add planet api key to .env file
PL_API_KEY=<PLANET_API_KEY>

```
make the command we need
```


TMUX

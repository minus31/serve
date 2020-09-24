import os
import sys
import glob

sys.path.append(os.getcwd()) # To help discover local modules
from scripts import tsutils

BASE_DIR = os.getcwd()

if tsutils.is_conda_env():
    print("Using conda to install torchserve and torch-model-archiver")
    channel_dir = os.path.abspath(os.path.join(BASE_DIR, "binaries", "conda", "output"))
    conda_cmd = f"conda install --channel {channel_dir} -y torchserve torch-model-archiver"
    print(f"Executing command: {conda_cmd}")
    INSTALL_EXIT_CODE = os.system(conda_cmd)
else:
    print("Using pip to install torchserve and torch-model-archiver")
    TS_WHEEL = glob.glob(os.path.join(BASE_DIR, "dist", "*.whl"))[0]
    MA_WHEEL = glob.glob(os.path.join(BASE_DIR, "model-archiver", "dist", "*.whl"))[0]
    pip_cmd = f"pip install {TS_WHEEL} {MA_WHEEL}"
    print(f"Executing command: {pip_cmd}")
    INSTALL_EXIT_CODE = os.system(pip_cmd)

if INSTALL_EXIT_CODE != 0 :
    sys.exit("Installation Failed")
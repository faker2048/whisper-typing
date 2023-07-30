# WhisperTyping

WhisperTyping is a voice input method based on `faster-whisper` technology. Press "Caps Lock" to start speaking and release it to obtain an English translation.
The result text will be automatically copied to your clipboard.

## Setup
```
pip install -r requirements.txt
```

## Run
```
cd .
python -m wstp.main --help
python -m wstp.main
```

## GPU Acceleration

For easy CUDA and cuDNN installation:
- Linux:
```bash
conda install cudnn
```

- Windows:

_Although using additional torch libraries may not be ideal, it's a straightforward approach for Windows (compared to Nvidia's official CUDA installation). Any alternative methods or suggestions are welcome!_
```bash
pip3 install torch --index-url https://download.pytorch.org/whl/cu118
```

After these settings, YTWS should work with a GPU.
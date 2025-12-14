# ACheese Trainer

ACheese is an external trainer for LORT steam game demo  
It works by reading/writing memory externally.

## Build It Yourself

If you don’t trust the prebuilt `.exe`, you can build ACheese yourself.

### Requirements

- Python **64-bit** (important)
- pip

### Dependencies

pip install pymem pyinstaller
Build Steps
Install Python and make sure it is added to PATH

Install the required dependencies:


pip install pymem pyinstaller

Place the following files in the same folder:

acheese.py

icon.ico (optional)

Build the executable:

bash

python -m PyInstaller --onefile --windowed --icon=icon.ico --name ACheese acheese.py


The compiled executable will be located at:
dist/ACheese.exe

Notes
The game must be running and you should be ingame or in the lobby before using the trainer.
also if you change the values the new value  only shows after you buy something or do something ingame.

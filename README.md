# ArgusScan 👁️‍🗨️
**The All-Seeing Camera Scanner**  
*Named after Argus Panoptes - The Hundred-Eyed Giant of Greek Mythology*


```bash
              +-------------------+
              |  Camera Network   |
              +--------+----------+
                       |
           +-----------v-----------+
           |      ArgusScan       |
           |  (The All-Seeing)    |
           +-----------+----------+
                       |
         +-------------v-------------+
         |   Discovered Cameras     |
         |   - Country Filtering    |
         |   - Accessibility Check  |
         |   - Multi-threaded Scan  |
         +---------------------------+
```

## ✨ Features

🌍 Country Scanning =>	Scan cameras in 100+ countries using ISO codes
⚡ Parallel Processing => Multi-threaded architecture for faster results
✅ Accessibility Check => Test which cameras are actually online and accessible
📁 Organized Output => Automatic saving to categorized text files
🎨 Colorized UI => Easy-to-read terminal interface with status colors
🔧 Customizable => Control scan depth, output format, and verbosity

![ArgusScan Terminal Demo](https://raw.githubusercontent.com/roxm337/ArgusScan/refs/heads/main/Screenshot%202025-05-22%20at%2010.38.37.png)
## 🛠️ Installation

Requirements

Python 3.8+
Linux/macOS/Windows (WSL recommended for Windows)

## Steps

# Clone repository
git clone https://github.com/roxm337/ArgusScan.git && cd ArgusScan

# Install dependencies
pip3 install -r requirements.txt

# Make executable
chmod +x arguscan.py

# Verify installation
./arguscan.py

🚀 Usage

Basic Command
```bash
python3 arguscan.py -c US  # Scan US cameras (saves to US_cameras.txt)
```

Full Options

Parameter | Description | Example
-c	Country code (required)	-c DE (Germany)
-o	Custom output filename	-o my_scan.txt
-p	Max pages to scan (default: all)	-p 3 (3 pages only)
-t	Test camera accessibility	-t (enable check)
-v	Verbose mode (show details)	-v
-h	Show help message	-h

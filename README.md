# CS7000 Convert GUI

Author:  Jason Johnson (k3jsj@arrl.net)</br>
Program revision: v1.3, February 7, 2026</br>

## Purpose
Application that converts an Anytone codeplug (Talk Group, Channels, and Zones) into Excel Spreadsheets for import into Connect Systems CPS software for CS7000 M17 Plus radio.

## CPS Dependencies
This version works with Anytone CPS version 3.04 and beyond. This version works with CS7000 M17 PLUS CPS version 1.2.19.00Beta and Firmware 9.00.93.

This version use the Table method in the Channels database.

## DISCLAIMER & TERMS OF USE
By using this software, you acknowledge and agree that you do so at your own risk. The author of this software makes no guarantees, representations, or warranties of any kind, express or implied, regarding the accuracy, reliability, or completeness of the software's output. The author shall not be held liable for any errors, omissions, or any losses, injuries, or damages arising from the use of this software.  Users are solely responsible for verifying the correctness of the software's output and for any decisions made based on such output.

Portions of this software are derived from open-source projects, and elements of the source code were generated using artificial intelligence. The author acknowledges the contributions of the open-source community and the advancements in AI technology that have made this software possible.

Source code for this applicaion is avaialble at
https://github.com/VikingNation/CS7000_convert_gui

Usage of the software reflects your acceptance of the terms of use.

## Usage
You can run the application by invoking the executable or by running "python CS700_convert_gui.py". The following are steps to convert the code plug.

### Anytone CPS
- Open your Anytone code plug in the Anytone CPS software.  Select Tools=>Export=>Export All.
- Pick the directory where you want to output all the files.  Type the filename for the LST file and click save button.

## Operating system command prompt
- Launch the gui executable (alternatively run python CS7000_convert_gui.py).
- Click the button to select the input folder of Anytone files.
- Click the button to select the output directory for the CS7000 spreadsheets.
- Select if you want to output digital + analog or digital only channels
- Select if you want to include the default Zones and Channels that come preinstalled with the CS7000.
- Finally, click the Convert Codeplug button

### CS7000 CPS
- Open the CS7000 CPS.
- Import the contacts spreadsheet
- Import the channels spreadsheet
- Import the zones spreadsheet
- Verify everthing imported correctly
- Following verification write to your radio

## Build instructions

### Dependencies
Using software from Python source code will require you to install the following software packages.

- Python 3 (with Tk)
- xlsxwriter
- openpyxl
- pyinstaller

Here are the steps to build the executable. Create your local Python environment, pip install the dependencies, and finally build the executable

$python -m venv venv

$venv\scripts\activate

$pip install -r requirements.txt

$pyinstaller --onefile CS7000_convert_gui.py --splash CS7000_splash_scaled.png -n CS7000_convert_gui-v1.3


The application will be in the dist folder.


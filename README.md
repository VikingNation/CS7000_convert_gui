# CS7000 Convert GUI

Author:  Jason Johnson (k3jsj@arrl.net)</br>
Program revision: v1.2, January 3, 2025</br>

## Purpose
Application that converts an Anytone codeplug (Talk Group, Channels, and Zones) into Excel Spreadsheets for import into Connect Systems CPS software for CS7000 M17 Plus radio.

## Executable
This application is avaialble as a pre-compiled executable for Windows 10/11.  That file is located here:</br>

<a href="https://github.com/VikingNation/CS7000_convert_gui/tree/main/dist/CS7000_convert_gui-v1.2.exe">CS7000_convert_gui-v1.2.exe</a> SHA256: 569217c361bb499afe82bdc2866450f877e1272b99bb0e141139560faf9796fc</br>
<a href="https://github.com/VikingNation/CS7000_convert_gui/tree/main/dist/CS7000_convert_gui-v1.2.exe.sig">CS70000_convert_gui-v1.2.exe.sig</a>


## DISCLAIMER & TERMS OF USE
By using this software, you acknowledge and agree that you do so at your own risk. The author of this software makes no guarantees, representations, or warranties of any kind, express or implied, regarding the accuracy, reliability, or completeness of the software's output. The author shall not be held liable for any errors, omissions, or any losses, injuries, or damages arising from the use of this software.  Users are solely responsible for verifying the correctness of the software's output and for any decisions made based on such output.

Portions of this software are derived from open-source projects, and elements of the source code were generated using artificial intelligence. The author acknowledges the contributions of the open-source community and the advancements in AI technology that have made this software possible.

Source code for this applicaion is avaialble at
https://github.com/VikingNation/CS7000_convert_gui

Usage of the software reflects your acceptance of the terms of use.

## Usage
The following are steps to use the program.

### Anytone CPS
- Open your Anytone code plug in the Anytone CPS software.  Select Tools=>Export=>Export All.
- Pick the directory where you want to output all the files.  Type the filename for the LST file and click save button.

## Operating system command prompt
- Launch the gui executable (alternatively run python CS7000_convert_gui.py).
- Click the button to select the input folder of Anytone files.
- Click the button to select the output directory for the CS7000 spreadsheets.
- Select if you want to output digital + analog or digital only channels
- Finally, click the Convert Codeplug button

### CS7000 CPS
- Open the CS7000 CPS.
- Import the contacts spreadsheet
- Import the channels spreadsheet
- Import the zones spreadsheet
- Verify everthing imported correctly

## Dependencies
Using software from Python source code will require you to install the following

- Python 3 (with Tk)
- xlsxwriter
- openpyxl

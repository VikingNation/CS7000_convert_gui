# CS7000 Code Plug Utilities

Author:  Jason Johnson (k3jsj@arrl.net)
Program revision 1.2, December 31, 2024

## Purpose
Application that converts an Anytone codeplug (Talk Group, Channels, and Zones) into Excel Spreadsheets that can be imported into Connect Systems CS7000 CPS software.

## DISCLAIMER & TERMS OF USE
By using this software, you acknowledge and agree that you do so at your own risk. The author of this software makes no guarantees, representations, or warranties of any kind, express or implied, regarding the accuracy, reliability, or completeness of the software's output. The author shall not be held liable for any errors, omissions, or any losses, injuries, or damages arising from the use of this software.  Users are solely responsible for verifying the correctness of the software's output and for any decisions made based on such output.

Portions of this software are derived from open-source projects, and elements of the source code were generated using artificial intelligence. The author acknowledges the contributions of the open-source community and the advancements in AI technology that have made this software possible.

Source code for this applicaion is avaialble at https://github.com/K3JSJ/CS7000

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

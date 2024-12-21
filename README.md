CS7000

Utilities to convert Anytone Talk Group, Channels, and Zones CSVs into the format to the CS7000 CPS uses in spreadsheets.

Current scripts only convert DMR channels.  Support to analog will be added at a future date.  See note below about need to tailor Anytone Zones CSV to account for fact that there will not be any analog channels improted

The recommended order of operations is:

- Open Anytone CPS and explort Talkgroups, Zones, and Channels
- Run scripts against talkgroups, zones, and channels to create CSVs that are opened and copied into the CPS7000 spreadsheet files
- Export Contacts, Channels, and Zones from CS7000 CPS software.
- Open convered talkgroups CSV in Excel and copy values.  Next, do a paste-special into the Contacts spreadsheet.  Save the file.
- Open the converted channels CSV in Excel and copy values.  Select the DMR channels worksheets.  Past special into the spreadsheet.  Save the file.
- Open the converted zones CSV in Excel and copy values.  Past special in to the zones spreadsheet. Save the file
- Open the CS7000 CPS and first import channels, then channels, then zones.  Double check to make sure everything is mapped correctly

Note:  The script to convert the channels detects DMR channels and only exports those at the moment.
Note:  Be sure you edit the Anytone Zones to convert before running the script to remove any zones that have analog channels


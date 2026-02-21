"""
Deduper.py
-----------
Centralized deduplication logic for Digital Contacts, Channels, and Zones
used by the CS7000_convert_gui application.

This module performs:
1. Duplicate Digital Contact detection and resolution
2. Duplicate Channel Name detection and resolution
3. Zone updates to reflect deduped channel names
4. Reporting of removed items

UI interactions (dialogs, prompts) are delegated to the UI layer.
"""

from collections import defaultdict
from connectSystems.CS7000.Channels import Channels
from connectSystems.CS7000.DigitalContacts import DigitalContacts
from connectSystems.CS7000.Zones import Zones
from ContactSelector import ContactSelector

class Deduper:
    """
    Deduper orchestrates the full deduplication workflow.

    Parameters
    ----------
    contacts : DigitalContacts
        The DigitalContacts storage object.
    channels : Channels
        The Channels storage object.
    zones : Zones
        The Zones storage object.
    ui : object
        UI interface providing:
            - ask_user_to_select_contact(duplicates)
            - ask_user_to_select_channel(duplicates)
            - show_message(text)
            - show_deleted_summary(contacts, channels)
    """

    def __init__(self, root, contacts, channels, zones, ui):
        self.contacts = contacts
        self.channels = channels
        self.zones = zones
        self.root = root

        # Tracking removed items for reporting
        self.contacts_deleted = []
        self.channels_deleted = []

        # Mapping for channel name replacements
        self.channel_replacements = {}



    def ask_user_to_select_contact(self, entries):
        dialog = ContactSelector(self.root, entries)
        dialog.wait_window()
        return dialog.selected
    # ----------------------------------------------------------------------
    # PUBLIC ENTRY POINT
    # ----------------------------------------------------------------------
    def run(self):
        """Run the full dedupe pipeline."""
        # Note we must delete duplicate channels first becuase for dedupe contacts we modify talk groups names
        #  If we do the contacts first this will cause issues with the search comparision
        self.channels.whereEndFirmware()
        self._dedupe_channels()
        self._dedupe_contacts()
        self._report()

    # ----------------------------------------------------------------------
    # CONTACT DEDUPLICATION
    # ----------------------------------------------------------------------
    def _dedupe_contacts(self):
        duplicates = self._find_contact_duplicates()

        if not duplicates:
            return

        for dmr_id, entries in duplicates.items():
            # For a given ID (Talkgroup/Contact ID) ask user which Alias they want to keep
            keep = self.ask_user_to_select_contact(entries)
            # Build list of rows that need deleting
            delete = [e for e in entries if e != keep]

            self.contacts_deleted.extend(delete)

            # Update channels referencing deleted contact aliases
            for d in delete:
                deleted_alias = d[2]
                self.channels.update_contact_name(deleted_alias, keep[2])

        # Remove deleted contacts
        for d in self.contacts_deleted:
            self.contacts.remove(d[2]) #Remove contact by name

    def _find_contact_duplicates(self):
        """Return dict of {dmr_id: [contact1, contact2, ...]} for duplicates."""
        groups = defaultdict(list)
        for c in self.contacts.get_all():
            groups[c[1]].append(c)

        return {dmr_id: lst for dmr_id, lst in groups.items() if len(lst) > 1}

    # ----------------------------------------------------------------------
    # CHANNEL DEDUPLICATION
    # ----------------------------------------------------------------------
    def _dedupe_channels(self):
        duplicates = self._find_channel_duplicates()

        if not duplicates:
            return
        for name, entries in duplicates.items():

            # Firmware channels are already de-duped
            #   If a firmware channel is first element than keep this and we will delete other channels
            if self.channels.isFirmwareChannel(entries[0]):
                keep = entries[0]
            else:
                # First element is not from firmware. Prompt user to select 
                #keep = self.ui.ask_user_to_select_channel(entries)
                keep = entries[0]

            # Process duplicate channels and build list of elements to delete
            delete = [e for e in entries if e != keep]

            # Record replacement mapping
            self.channel_replacements[name] = keep[1]

            # Remove deleted channels
            for d in delete:
                self.channels.remove(d)
                self.channels_deleted.append(d)

    def _find_channel_duplicates(self):
        """Return dict of {channel_name: [channel1, channel2, ...]} for duplicates."""
        groups = defaultdict(list)
        for ch in self.channels.get_all():
            groups[ch[1]].append(ch)

        return {name: lst for name, lst in groups.items() if len(lst) > 1}

    # ----------------------------------------------------------------------
    # ZONE UPDATE (UPDATED FOR YOUR ZONES IMPLEMENTATION)
    # ----------------------------------------------------------------------
    def _update_zones(self):
        """
        Replace deleted channel names in all zones using the Zones.replace_channel() method.
        """
        if not self.channel_replacements:
            return

        for old_name, new_name in self.channel_replacements.items():
            self.zones.replace_channel(old_name, new_name)

    # ----------------------------------------------------------------------
    # REPORTING
    # ----------------------------------------------------------------------
    def _report(self):
        """Show summary of removed items or notify if nothing was removed."""

        if not self.contacts_deleted:
            return

        print(f"Removed the following contacts")
        for e in self.contacts_deleted:
            print(f"{e}")
        print("\n")

        print(f"Removed the following channels ({len(self.channels_deleted)})")
        for e in self.channels_deleted:
            print(f"{e}")
        print("\n")

        return
        if not self.contacts_deleted and not self.channels_deleted:
            self.ui.show_message("No duplicate contacts or channels were found.")
            return

        self.ui.show_deleted_summary(
            contacts=self.contacts_deleted,
            channels=self.channels_deleted
        )


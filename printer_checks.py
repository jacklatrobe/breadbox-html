#!/usr/bin/env python3

import pandas as pd
import sys

# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

# Print error function
def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Main check logic
class PrinterCheck(AgentCheck):
    def check(self, instance):
        # Printer base IP / URL
        printer_address = "http://192.168.0.112/"
        csv_location = "{}etc/mnt_info.csv".format(printer_address)

        # Load CSV data
        try:
            csv_data = pd.read_csv(csv_location)
            printer_data = {
                "node_name" : csv_data.loc[0, "Node Name"],
                "drum_left" : csv_data.loc[0, "% of Life Remaining(Drum Unit)"],
                "toner_left" : csv_data.loc[0, "% of Life Remaining(Toner)"],
                "pages_printed" : csv_data.loc[0, "Plain/Thin/Recycled"],
                "pages_jammed" : csv_data.loc[0, "Total Paper Jams"]
            }
        except:
            print_error("Error: Unable to read CSV from URL")
            sys.exit(1)

        # Printer gauges
        default_tags = tags=["DEVICE:{}".format(printer_data["node_name"]),'ENV:HOUSEHOLD'] + self.instance.get('tags', [])
        self.gauge('household.printer.drum_left', printer_data["drum_left"],tags=default_tags)
        self.gauge('household.printer.toner_left', printer_data["drum_left"],tags=default_tags)
        self.gauge('household.printer.pages_printed', printer_data["drum_left"],tags=default_tags)
        self.gauge('household.printer.pages_jammed', printer_data["drum_left"],tags=default_tags)
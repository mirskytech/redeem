from __future__ import absolute_import
"""
GCode G28
Steppers homing

Author: Mathieu Monney
email: zittix(at)xwaves(dot)net
Website: http://www.xwaves.net
License: CC BY-SA: http://creativecommons.org/licenses/by-sa/2.0/
"""

import logging

from .GCodeCommand import GCodeCommand
from redeem.Path import G92Path


class G28(GCodeCommand):

    def execute(self, g):
        if g.num_tokens() == 0:  # If no token is given, home all
            g.set_tokens(["X0", "Y0", "Z0", "E0", "H0"])
        
        axis_home = []
        
        for i in range(g.num_tokens()):  # Run through all tokens
            axis = g.token_letter(i)
            if axis.upper() in self.printer.AXES and self.printer.config.getboolean(
                'Endstops','has_' + axis.lower()):
                axis_home.append(axis)

        if len(axis_home):
            self.printer.path_planner.wait_until_done()
            self.printer.path_planner.home(axis_home)
            if g.has_letter("M"):
                #matrix = self.printer.path_planner.prev.end_pos[:3].dot(self.printer.matrix_bed_comp)
                current = self.printer.path_planner.get_current_pos(mm=False, ideal=True)
                p = G92Path({"Z": current["Z"]}, cancelable=False, use_bed_matrix=True)
                self.printer.path_planner.add_path(p)
    
        logging.info("Homing done.")
        self.printer.send_message(g.prot, "Homing done.")

    def get_description(self):
        return "Move the steppers to their homing position (and find it as " \
               "well)"

    def get_long_description(self):
        return ("Move the steppers to their homing position. "
                "The printer will travel a maximum length and direction"
                "defined by travel_*. Delta printers will home both X, Y and Z "
                "regardless of whicho of those axes were specified to home."
                "For other printers, one or more axes can be specified. An axis will "
                "only be homed if homing of that axis is enabled.\n"
                "M = Add the offset from the Z-axis provided by the bed matrix")

    def is_buffered(self):
        return True

    def get_test_gcodes(self):
        return ["G28"]

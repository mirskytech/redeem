import inspect

from docutils import nodes
from sphinx import addnodes
from docutils.parsers import rst

from docs.ext.gcodes.nodes import GCodeNode, GCodeDescriptionNode, GCodeLongDescriptionNode


class GCodeDirective(rst.Directive):

    name = 'gcodes'

    def load_classes_in_module(self, module):
        from redeem.gcodes.GCodeCommand import GCodeCommand
        for module_name, obj in inspect.getmembers(module):

            if inspect.ismodule(obj) and (obj.__name__.startswith('gcodes') or obj.__name__.startswith('redeem.gcodes')):
                self.load_classes_in_module(obj)
            elif inspect.isclass(obj) and issubclass(obj, GCodeCommand) and module_name != 'GCodeCommand' and module_name != 'ToolChange':

                print("got gcode, wohoo {}".format(obj.__name__))

    def run(self):

        from redeem.gcodes.G1_G0 import G0
        gcode = G0(None)

        gcode_node = GCodeNode()
        gcode_node['gcode'] = gcode

        description = GCodeDescriptionNode()
        description['description'] = gcode.get_description()
        gcode_node += description

        long_description = GCodeLongDescriptionNode()
        long_description['long-description'] = gcode.get_long_description()
        gcode_node += long_description

        section = nodes.section()
        section += nodes.title(type(gcode).__name__, type(gcode).__name__)

        target = nodes.target()
        lineno = self.state_machine.abs_line_number()
        self.state.add_target(type(gcode).__name__, '', target, lineno)

        return [target, section, gcode_node, ]


# from __future__ import absolute_import
import os
import glob
# from importlib import import_module

# Import all python files as submodule
for f in glob.glob(os.path.dirname(__file__) + "/*.py"):
    if os.path.isfile(f) and not f.endswith('__init__.py') and \
            not f.endswith('GCodeCommand.py'):
        moduleName = os.path.splitext(os.path.basename(f))[0]
        __import__(moduleName, locals(), globals())

# import sys
#
# gcode_module = sys.modules[__name__]
#
# # FIXME : py3
# # from importlib import import_module
# for f in glob.glob(os.path.dirname(__file__) + "/*.py"):
#     if os.path.isfile(f) and not f.endswith('__init__.py') and \
#             not f.endswith('GCodeCommand.py'):
#         moduleName = os.path.splitext(os.path.basename(f))[0]
#         mod = import_module("redeem.gcodes.{}".format(moduleName), '')
#         setattr(gcode_module, moduleName, mod)

# ---------------
# RedeemConfig.py

from abc import abstractmethod

from CascadingConfigParser import CascadingConfigParser


class ConfigBase(object):
    """Superclass of all config 'sections'"""

    def get(self, key):
        if not getattr(self, key, None):
            return None
        return getattr(self, key)

    def getfloat(self, key):
        val = self.get(key)
        try:
            val = float(val)
        except ValueError:
            return None
        return val

    def getint(self, key):
        val = self.get(key)
        try:
            val = int(val)
        except ValueError:
            return None
        return val


class StepperConfig(ConfigBase):
    """Define the attributes that redeem expects to be available in the stepper section"""

    microstepping_x = 3
    microstepping_y = 3
    microstepping_z = 3
    # .
    # .
    # .


class PlannerConfig(ConfigBase):

    acceleration_x = 0.5
    # .
    # .
    # .

    max_jerk_x = 0.01
    max_jerk_y = 0.01
    # .
    # .
    # .


class RedeemConfig(object):
    """match the 'interface' for the ConfigParser to minimize the need
    to update where `printer.config` is accessed in the code base.
    """
    stepper = StepperConfig()
    planner = PlannerConfig()
    # system = SystemConfig
    # .
    # .
    # .

    def get(self, section, key):
        if hasattr(self, section.lower()):
            return getattr(self, section.lower()).get(key)
        return None

    def getint(self, section, key):
        if hasattr(self, section.lower()):
            return getattr(self, section.lower()).getint(key)
        return None

    def getfloat(self, section, key):
        if hasattr(self, section.lower()):
            return getattr(self, section.lower()).getfloat(key)
        return None

    def getboolean(self, section, key):
        if hasattr(self, section.lower()):
            return getattr(self, section.lower()).getboolean(key)
        return None

# ----------------
# ConfigFactory.py


class ConfigFactory(object):

    cpp = None
    sections = [
        ('Steppers', StepperConfig),
        ('Planner', PlannerConfig),
        # ...
    ]

    def __init__(self, config_files):
        self.ccp = CascadingConfigParser(config_files)

    def hydrate_config(self):

        redeem_config = RedeemConfig()
        for section_name, section_cls in self.sections:
            hydration_name = 'hydrate_' + section_cls.__name__.lower()
            if hasattr(self, hydration_name):
                config_func = getattr(self, hydration_name)
                config = config_func()
            else:
                config = self.hydrate_section_config(section_name, section_cls)

            setattr(redeem_config, section_name.lower(), config)

        return redeem_config

    def hydrate_section_config(self, section_name, config_cls):
        """A simple mapper from ini to config class"""
        config = config_cls()
        for item in config_cls.__dict__:
            if item.startswith('__'):
                continue
            setattr(config, item, self.ccp.get(section_name, item))
        return config


class ConfigV19Factory(ConfigFactory):
    """Uses the default behavior for all sections"""
    pass


class ConfigV20Factory(ConfigFactory):
    """Redefines behavior for a specific configuration section"""

    def hydrate_plannerconfig(self):
        """A mapper that renames certain keys to new names or adjusts values to new units (eg)"""
        pcfg = PlannerConfig()
        for item in StepperConfig.__dict__:
            if item.startswith('__'):
                continue

            # example of name adjustment
            if item.startswith('max_jerk_'):
                item = item.replace('max_jerk_', 'max_speed_jump_')

            value = self.cpp.get('Planner', item)

            # example of value adjustment (from m/s to mm/s)
            if item.startswith('max_speed_'):
                value = value * 1000

            setattr(pcfg, item, value)
        return pcfg


# -------------

configs = ['configs/default.cfg', 'configs/printer.cfg', 'configs/local.cfg']
ccp = CascadingConfigParser(configs)
config_version = '1.9'
if ccp.has_option('System', 'config_version'):
    config_version = ccp.get('System', 'config_version')

if config_version not in ['1.9', '2.0',]:
    raise Exception("unrecognized version")

factory = None

if config_version == '2.0':
    factory = ConfigV20Factory(configs)
else:
    factory = ConfigV19Factory(configs)

# printer.cfg = factory.hydrate_config()

#
#
#     def get(self, key):
#         if not getattr(self, key, None):
#             return None
#         val = getattr(self, key)
#
#         if type(val) is
#
#
#
#     endstop_x1 = EndstopTypeEnum.na  # type: EndstopTypeEnum
#     endstop_x2 = EndstopTypeEnum.na  # type: EndstopTypeEnum
#     endstop_y1 = EndstopTypeEnum.na  # type: EndstopTypeEnum
#     # .
#     # .
#     # .
#
# # -------------
# # enums.py
#
# from enum import Enum
#
#
# class StepperDirectionEnum(ConfigBase):
#     X_CW = 1
#     X_CCW = 2
#     X_POS = 3
#     X_NEG = 4
#
#
# class EndstopTypeEnum(Enum):
#     na = 1  # not available
#     no = 2  # normally open
#     nc = 3  # normally closed

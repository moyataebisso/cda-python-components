#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# You may find it more helpful to your design to adjust the
# functionality, constants and interfaces (if there are any)
# provided within in order to meet the needs of your specific
# Programming the Internet of Things project.
# 

import logging

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

from sense_emu import SenseHat

class HvacEmulatorTask(BaseActuatorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		super().__init__(actuatorType = ConfigConst.HVAC_ACTUATOR_TYPE, 
						simpleName = "HVAC")
		
		self.sh = SenseHat()
		logging.info("HvacEmulatorTask initialized with SenseHat emulator")

	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
		Activate the HVAC emulator by displaying blue (cooling) or red (heating) on LED matrix.
		"""
		logging.info("Activating HVAC emulator with value: %f", val)
		
		if val < 20.0:
			# Heating mode - display red
			self.sh.clear(255, 0, 0)
			self.sh.show_letter('H', text_colour=[255, 0, 0])
		else:
			# Cooling mode - display blue
			self.sh.clear(0, 0, 255)
			self.sh.show_letter('C', text_colour=[0, 0, 255])
		
		sleep(2)
		
		if val < 20.0:
			self.sh.clear(255, 0, 0)
		else:
			self.sh.clear(0, 0, 255)
		
		return 0

	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
		Deactivate the HVAC emulator by clearing the LED matrix.
		"""
		logging.info("Deactivating HVAC emulator")
		
		# Clear the LED matrix
		self.sh.clear()
		
		return 0
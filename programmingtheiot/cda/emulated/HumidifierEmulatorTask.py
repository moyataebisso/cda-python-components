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

class HumidifierEmulatorTask(BaseActuatorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		super().__init__(actuatorType = ConfigConst.HUMIDIFIER_ACTUATOR_TYPE, 
						simpleName = "HUMIDIFIER")
		
		self.sh = SenseHat()
		logging.info("HumidifierEmulatorTask initialized with SenseHat emulator")

	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
		Activate the humidifier emulator by displaying green on LED matrix.
		"""
		logging.info("Activating humidifier emulator with value: %f", val)
		
		# Display green color for humidifier ON
		self.sh.clear(0, 255, 0)
		
		# Optional: Display 'H' for Humidifier
		self.sh.show_letter('H', text_colour=[0, 255, 0])
		sleep(2)
		self.sh.clear(0, 255, 0)
		
		return 0

	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
		Deactivate the humidifier emulator by clearing the LED matrix.
		"""
		logging.info("Deactivating humidifier emulator")
		
		# Clear the LED matrix
		self.sh.clear()
		
		return 0
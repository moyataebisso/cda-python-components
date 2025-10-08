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

from programmingtheiot.data.SensorData import SensorData

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask

from sense_emu import SenseHat

class PressureSensorEmulatorTask(BaseSensorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, dataSet = None):
		super().__init__(sensorType = ConfigConst.PRESSURE_SENSOR_TYPE, 
						dataSet = dataSet,
						minVal = 900.0,
						maxVal = 1100.0)
		
		self.sh = SenseHat()
		logging.info("PressureSensorEmulatorTask initialized with SenseHat emulator")
	
	def generateTelemetry(self) -> float:
		"""
		Generate telemetry by reading from the Sense HAT emulator.
		
		@return float The pressure reading from the emulator
		"""
		pressure = self.sh.get_pressure()
		self.latestSensorData = SensorData(typeID = self.sensorType)
		self.latestSensorData.setValue(pressure)
		self.latestSensorData.setName(ConfigConst.PRESSURE_SENSOR_NAME)
		
		logging.debug("Generated pressure emulator data: %f", pressure)
		
		return pressure
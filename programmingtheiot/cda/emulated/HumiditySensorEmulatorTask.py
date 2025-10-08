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

class HumiditySensorEmulatorTask(BaseSensorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, dataSet = None):
		super().__init__(sensorType = ConfigConst.HUMIDITY_SENSOR_TYPE, 
						dataSet = dataSet,
						minVal = ConfigConst.DEFAULT_VAL,
						maxVal = 100.0)
		
		self.sh = SenseHat()
		logging.info("HumiditySensorEmulatorTask initialized with SenseHat emulator")
	
	def generateTelemetry(self) -> float:
		"""
		Generate telemetry by reading from the Sense HAT emulator.
		
		@return float The humidity reading from the emulator
		"""
		humidity = self.sh.get_humidity()
		self.latestSensorData = SensorData(typeID = self.sensorType)
		self.latestSensorData.setValue(humidity)
		self.latestSensorData.setName(ConfigConst.HUMIDITY_SENSOR_NAME)
		
		logging.debug("Generated humidity emulator data: %f", humidity)
		
		return humidity
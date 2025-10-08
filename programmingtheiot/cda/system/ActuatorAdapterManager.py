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

from importlib import import_module

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.ActuatorData import ActuatorData

from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask

class ActuatorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""
	
	def __init__(self):
		self.configUtil = ConfigUtil()
		
		self.useEmulator = self.configUtil.getBoolean(
			section = ConfigConst.CONSTRAINED_DEVICE,
			key = ConfigConst.ENABLE_EMULATOR_KEY)
		
		self.locationID = self.configUtil.getProperty(
			section = ConfigConst.CONSTRAINED_DEVICE,
			key = ConfigConst.DEVICE_LOCATION_ID_KEY,
			defaultVal = ConfigConst.NOT_SET)
		
		self.dataMsgListener = None
		
		# Initialize actuator tasks
		if not self.useEmulator:
			self.humidifierActuator = HumidifierActuatorSimTask()
			self.hvacActuator = HvacActuatorSimTask()

	def sendActuatorCommand(self, data: ActuatorData) -> bool:
		if data and not data.isResponseFlagEnabled():
			if data.getLocationID() == self.locationID:
				logging.info('Processing actuator command for loc ID %s.', 
						   str(data.getLocationID()))
				
				aType = data.getTypeID()
				responseData = None
				
				if aType == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE and hasattr(self, 'humidifierActuator'):
					responseData = self.humidifierActuator.updateActuator(data)
				elif aType == ConfigConst.HVAC_ACTUATOR_TYPE and hasattr(self, 'hvacActuator'):
					responseData = self.hvacActuator.updateActuator(data)
				else:
					logging.warning('No valid actuator for type: %s', aType)
				
				if responseData and self.dataMsgListener:
					self.dataMsgListener.handleActuatorCommandResponse(responseData)
					return True
			else:
				logging.warning('Invalid location ID: %s', str(data.getLocationID()))
		else:
			logging.warning('Invalid actuator msg. Ignoring.')
		
		return False
	
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		if listener:
			self.dataMsgListener = listener
			return True
		return False
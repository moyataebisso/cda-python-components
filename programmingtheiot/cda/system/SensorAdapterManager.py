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

from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask
from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask

class SensorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		self.configUtil = ConfigUtil()
		
		self.pollRate = self.configUtil.getInteger(
			section = ConfigConst.CONSTRAINED_DEVICE,
			key = ConfigConst.POLL_CYCLES_KEY,
			defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)
		
		self.useEmulator = self.configUtil.getBoolean(
			section = ConfigConst.CONSTRAINED_DEVICE,
			key = ConfigConst.ENABLE_EMULATOR_KEY)
		
		self.locationID = self.configUtil.getProperty(
			section = ConfigConst.CONSTRAINED_DEVICE,
			key = ConfigConst.DEVICE_LOCATION_ID_KEY,
			defaultVal = ConfigConst.NOT_SET)
		
		if self.pollRate <= 0:
			self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
		
		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job(self.handleTelemetry, 'interval', seconds = self.pollRate)
		
		self.dataMsgListener = None
		
		# Initialize sensor tasks
		if not self.useEmulator:
			self.dataGenerator = SensorDataGenerator()
			
			# Temperature sensor
			tempFloor = self.configUtil.getFloat(
				section = ConfigConst.CONSTRAINED_DEVICE,
				key = ConfigConst.TEMP_SIM_FLOOR_KEY,
				defaultVal = SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP)
			
			tempCeiling = self.configUtil.getFloat(
				section = ConfigConst.CONSTRAINED_DEVICE,
				key = ConfigConst.TEMP_SIM_CEILING_KEY,
				defaultVal = SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
			
			tempData = self.dataGenerator.generateDailyIndoorTemperatureDataSet(
				minValue = tempFloor,
				maxValue = tempCeiling,
				useSeconds = False)
			
			self.tempAdapter = TemperatureSensorSimTask(dataSet = tempData)
			
			# Humidity sensor
			humidityData = self.dataGenerator.generateDailyEnvironmentHumidityDataSet()
			self.humidityAdapter = HumiditySensorSimTask(dataSet = humidityData)
			
			# Pressure sensor
			pressureData = self.dataGenerator.generateDailyEnvironmentPressureDataSet()
			self.pressureAdapter = PressureSensorSimTask(dataSet = pressureData)

	def handleTelemetry(self):
		if not self.useEmulator:
			humidityData = self.humidityAdapter.generateTelemetry()
			pressureData = self.pressureAdapter.generateTelemetry()
			tempData = self.tempAdapter.generateTelemetry()
			
			# Set location ID
			humidityData.setLocationID(self.locationID)
			pressureData.setLocationID(self.locationID)
			tempData.setLocationID(self.locationID)
			
			logging.info('Generated humidity data: %s', str(humidityData))
			logging.info('Generated pressure data: %s', str(pressureData))
			logging.info('Generated temp data: %s', str(tempData))
			
			if self.dataMsgListener:
				self.dataMsgListener.handleSensorMessage(humidityData)
				self.dataMsgListener.handleSensorMessage(pressureData)
				self.dataMsgListener.handleSensorMessage(tempData)
		
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		if listener:
			self.dataMsgListener = listener
			return True
		return False
	
	def startManager(self):
		logging.info('Started SensorAdapterManager.')
		if not self.scheduler.running:
			self.scheduler.start()
		else:
			logging.warning('SensorAdapterManager scheduler already started.')
		
	def stopManager(self):
		logging.info('Stopped SensorAdapterManager.')
		try:
			self.scheduler.shutdown()
		except:
			logging.warning('SensorAdapterManager scheduler already stopped.')
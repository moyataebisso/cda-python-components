#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#

import logging
from apscheduler.schedulers.background import BackgroundScheduler
from importlib import import_module

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.SensorData import SensorData

# Import simulator tasks
from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask
from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask

# Import data generator
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator

class SensorAdapterManager(object):
    """
    Sensor adapter manager implementation.
    """
    
    def __init__(self):
        self.configUtil = ConfigUtil()
        
        self.pollRate = self.configUtil.getInteger(
            section = ConfigConst.CONSTRAINED_DEVICE,
            key = ConfigConst.POLL_CYCLES_KEY,
            defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)
        
        if self.pollRate <= 0:
            self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
        
        self.useEmulator = self.configUtil.getBoolean(
            section = ConfigConst.CONSTRAINED_DEVICE,
            key = ConfigConst.ENABLE_EMULATOR_KEY)
        
        self.locationID = self.configUtil.getProperty(
            section = ConfigConst.CONSTRAINED_DEVICE,
            key = ConfigConst.DEVICE_LOCATION_ID_KEY,
            defaultVal = ConfigConst.NOT_SET)
        
        self.dataMsgListener = None
        
        # Initialize scheduler
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.handleTelemetry, 'interval', seconds = self.pollRate)
        
        # Initialize environmental sensor tasks
        self._initEnvironmentalSensorTasks()
        
        logging.info("Sensor location ID: %s", self.locationID)
    
    def _initEnvironmentalSensorTasks(self):
        """
        Initialize environmental sensor tasks based on configuration.
        """
        if not self.useEmulator:
            logging.info("SensorAdapterManager is using simulator tasks.")
            
            # Load simulator data sets
            self.dataGenerator = SensorDataGenerator()
            
            humidityFloor = self.configUtil.getFloat(
                section = ConfigConst.CONSTRAINED_DEVICE, 
                key = ConfigConst.HUMIDITY_SIM_FLOOR_KEY,
                defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY)
            humidityCeiling = self.configUtil.getFloat(
                section = ConfigConst.CONSTRAINED_DEVICE, 
                key = ConfigConst.HUMIDITY_SIM_CEILING_KEY,
                defaultVal = SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY)
            
            pressureFloor = self.configUtil.getFloat(
                section = ConfigConst.CONSTRAINED_DEVICE, 
                key = ConfigConst.PRESSURE_SIM_FLOOR_KEY,
                defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
            pressureCeiling = self.configUtil.getFloat(
                section = ConfigConst.CONSTRAINED_DEVICE, 
                key = ConfigConst.PRESSURE_SIM_CEILING_KEY,
                defaultVal = SensorDataGenerator.HI_NORMAL_ENV_PRESSURE)
            
            tempFloor = self.configUtil.getFloat(
                section = ConfigConst.CONSTRAINED_DEVICE, 
                key = ConfigConst.TEMP_SIM_FLOOR_KEY,
                defaultVal = SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP)
            tempCeiling = self.configUtil.getFloat(
                section = ConfigConst.CONSTRAINED_DEVICE, 
                key = ConfigConst.TEMP_SIM_CEILING_KEY,
                defaultVal = SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
            
            # Generate data sets
            humidityData = self.dataGenerator.generateDailyEnvironmentHumidityDataSet(
                minValue = humidityFloor, maxValue = humidityCeiling, useSeconds = False)
            pressureData = self.dataGenerator.generateDailyEnvironmentPressureDataSet(
                minValue = pressureFloor, maxValue = pressureCeiling, useSeconds = False)
            tempData = self.dataGenerator.generateDailyIndoorTemperatureDataSet(
                minValue = tempFloor, maxValue = tempCeiling, useSeconds = False)
            
            # Create simulator tasks
            self.humidityAdapter = HumiditySensorSimTask(dataSet = humidityData)
            self.pressureAdapter = PressureSensorSimTask(dataSet = pressureData)
            self.tempAdapter = TemperatureSensorSimTask(dataSet = tempData)
        else:
            logging.info("SensorAdapterManager is using emulator tasks.")
            
            # Dynamically load emulator modules
            heModule = import_module('programmingtheiot.cda.emulated.HumiditySensorEmulatorTask', 
                                    'HumiditySensorEmulatorTask')
            heClazz = getattr(heModule, 'HumiditySensorEmulatorTask')
            self.humidityAdapter = heClazz()
            
            peModule = import_module('programmingtheiot.cda.emulated.PressureSensorEmulatorTask', 
                                    'PressureSensorEmulatorTask')
            peClazz = getattr(peModule, 'PressureSensorEmulatorTask')
            self.pressureAdapter = peClazz()
            
            teModule = import_module('programmingtheiot.cda.emulated.TemperatureSensorEmulatorTask', 
                                    'TemperatureSensorEmulatorTask')
            teClazz = getattr(teModule, 'TemperatureSensorEmulatorTask')
            self.tempAdapter = teClazz()
    
    def handleTelemetry(self):
        """
        Handle telemetry generation for all sensors.
        """
        # Generate telemetry - returns SensorData objects
        tempData = self.tempAdapter.generateTelemetry()
        humiData = self.humidityAdapter.generateTelemetry()
        pressData = self.pressureAdapter.generateTelemetry()
        
        # Set location ID for all data objects
        tempData.setLocationID(self.locationID)
        humiData.setLocationID(self.locationID)
        pressData.setLocationID(self.locationID)
        
        # Log the generated data
        logging.info('Generated temp data: %s', str(tempData))
        logging.info('Generated humidity data: %s', str(humiData))
        logging.info('Generated pressure data: %s', str(pressData))
        
        # Send to listener if available
        if self.dataMsgListener:
            self.dataMsgListener.handleSensorMessage(tempData)
            self.dataMsgListener.handleSensorMessage(humiData)
            self.dataMsgListener.handleSensorMessage(pressData)
    
    def setDataMessageListener(self, listener: IDataMessageListener):
        """
        Set the data message listener for callbacks.
        
        @param listener The IDataMessageListener instance
        """
        if listener:
            self.dataMsgListener = listener
    
    def startManager(self):
        """
        Start the sensor adapter manager.
        """
        logging.info("Started SensorAdapterManager.")
        
        if not self.scheduler.running:
            self.scheduler.start()
        else:
            logging.warning("SensorAdapterManager scheduler already started.")
    
    def stopManager(self):
        """
        Stop the sensor adapter manager.
        """
        logging.info("Stopped SensorAdapterManager.")
        
        try:
            self.scheduler.shutdown()
        except:
            logging.warning("SensorAdapterManager scheduler already stopped.")
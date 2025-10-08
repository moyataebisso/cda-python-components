#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#

import logging
from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.SensorData import SensorData

# Import simulator tasks
from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask
from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask

# Import emulator tasks
from programmingtheiot.cda.emulated.TemperatureSensorEmulatorTask import TemperatureSensorEmulatorTask
from programmingtheiot.cda.emulated.HumiditySensorEmulatorTask import HumiditySensorEmulatorTask
from programmingtheiot.cda.emulated.PressureSensorEmulatorTask import PressureSensorEmulatorTask

# Import data generator
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator

class SensorAdapterManager(object):
    """
    Sensor adapter manager implementation.
    """
    
    def __init__(self):
        configUtil = ConfigUtil()
        
        self.pollRate = configUtil.getInteger(
            section = ConfigConst.CONSTRAINED_DEVICE,
            key = ConfigConst.POLL_CYCLES_KEY,
            defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)
        
        if self.pollRate <= 0:
            self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
        
        self.useEmulator = configUtil.getBoolean(
            section = ConfigConst.CONSTRAINED_DEVICE,
            key = ConfigConst.ENABLE_EMULATOR_KEY)
        
        self.locationID = configUtil.getProperty(
            section = ConfigConst.CONSTRAINED_DEVICE,
            key = ConfigConst.DEVICE_LOCATION_ID_KEY,
            defaultVal = ConfigConst.NOT_SET)
        
        self.dataMsgListener = None
        
        # Initialize scheduler
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.handleTelemetry, 'interval', seconds = self.pollRate)
        
        # Initialize sensor tasks based on emulator setting
        if self.useEmulator:
            logging.info("SensorAdapterManager is using emulator tasks.")
            
            try:
                self.tempSensor = TemperatureSensorEmulatorTask()
                self.humiSensor = HumiditySensorEmulatorTask()
                self.presSensor = PressureSensorEmulatorTask()
                logging.info("Successfully initialized emulator sensors")
            except Exception as e:
                logging.error("Failed to initialize emulator sensors: %s", str(e))
                logging.info("Falling back to simulator tasks")
                self._initSimulatorTasks()
        else:
            logging.info("SensorAdapterManager is using simulator tasks.")
            self._initSimulatorTasks()
        
        logging.info("Sensor location ID: %s", self.locationID)
    
    def _initSimulatorTasks(self):
        """
        Initialize simulator tasks - simplest working approach from Lab Module 03.
        """
        # Simple initialization without data sets - this worked in Lab Module 03
        self.tempSensor = TemperatureSensorSimTask()
        self.humiSensor = HumiditySensorSimTask()
        self.presSensor = PressureSensorSimTask()
    
    def handleTelemetry(self):
        """
        Handle telemetry generation for all sensors.
        """
        # Generate telemetry - returns SensorData objects
        tempData = self.tempSensor.generateTelemetry()
        humiData = self.humiSensor.generateTelemetry()
        pressData = self.presSensor.generateTelemetry()
        
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
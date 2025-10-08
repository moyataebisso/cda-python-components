#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#
# Copyright (c) 2020 - 2025 by Andrew D. King
#

import logging
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager
from programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DeviceDataManager(IDataMessageListener):
    """
    Device data manager - orchestrates all data flow.
    """
    
    def __init__(self):
        """
        Constructor.
        """
        self.configUtil = ConfigUtil()
        
        # Initialize managers
        self.sysPerfMgr = SystemPerformanceManager()
        self.sysPerfMgr.setDataMessageListener(self)
        
        self.sensorAdapterMgr = SensorAdapterManager()
        self.sensorAdapterMgr.setDataMessageListener(self)
        
        self.actuatorAdapterMgr = ActuatorAdapterManager()
        self.actuatorAdapterMgr.setDataMessageListener(self)
        
        # Load temperature control settings
        self.enableHandleTempChangeOnDevice = self.configUtil.getBoolean(
            section = ConfigConst.CONSTRAINED_DEVICE,
            key = ConfigConst.HANDLE_TEMP_CHANGE_ON_DEVICE_KEY)
        
        self.triggerHvacTempFloor = self.configUtil.getFloat(
            section = ConfigConst.CONSTRAINED_DEVICE,
            key = ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY,
            defaultVal = 18.0)
        
        self.triggerHvacTempCeiling = self.configUtil.getFloat(
            section = ConfigConst.CONSTRAINED_DEVICE,
            key = ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY,
            defaultVal = 22.0)
    
    def startManager(self):
        """
        Start the manager.
        """
        logging.info("Started DeviceDataManager.")
        self.sysPerfMgr.startManager()
        self.sensorAdapterMgr.startManager()
    
    def stopManager(self):
        """
        Stop the manager.
        """
        logging.info("Stopped DeviceDataManager.")
        self.sysPerfMgr.stopManager()
        self.sensorAdapterMgr.stopManager()
    
    def handleSensorMessage(self, data: SensorData) -> bool:
        """
        Handle sensor message.
        """
        if data:
            logging.info("Incoming sensor data received: %s", str(data))
            self._handleSensorDataAnalysis(data)
            return True
        
        logging.warning("Invalid sensor data. Ignoring.")
        return False
    
    def _handleSensorDataAnalysis(self, data: SensorData):
        """
        Analyze sensor data and trigger actuation if needed.
        """
        if self.enableHandleTempChangeOnDevice and data.getTypeID() == ConfigConst.TEMP_SENSOR_TYPE:
            ad = ActuatorData(typeID = ConfigConst.HVAC_ACTUATOR_TYPE)
            ad.setLocationID(data.getLocationID())
            
            if data.getValue() > self.triggerHvacTempCeiling:
                ad.setCommand(ConfigConst.COMMAND_ON)
                ad.setValue(self.triggerHvacTempCeiling)
            elif data.getValue() < self.triggerHvacTempFloor:
                ad.setCommand(ConfigConst.COMMAND_ON)
                ad.setValue(self.triggerHvacTempFloor)
            else:
                ad.setCommand(ConfigConst.COMMAND_OFF)
            
            self.handleActuatorCommandMessage(ad)
    
    def handleActuatorCommandMessage(self, data: ActuatorData) -> bool:
        """
        Handle actuator command message.
        """
        if data:
            logging.debug("Processing actuator command.")
            self.actuatorAdapterMgr.sendActuatorCommand(data)
            return True
        
        logging.warning("Invalid actuator command.")
        return False
    
    def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:
        """
        Handle actuator command response.
        """
        logging.debug("Actuator response received: %s", str(data))
        return True
    
    def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
        """
        Handle system performance message.
        """
        logging.debug("System performance data received: %s", str(data))
        return True
    
    def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
        """
        Handle incoming message.
        """
        logging.debug("Incoming message received.")
        return True
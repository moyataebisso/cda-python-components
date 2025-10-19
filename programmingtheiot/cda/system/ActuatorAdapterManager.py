#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#

import logging

from importlib import import_module

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.ActuatorData import ActuatorData

# Import simulator tasks
from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask

class ActuatorAdapterManager(object):
    """
    Actuator adapter manager implementation.
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
        
        # Initialize environmental actuation tasks
        self._initEnvironmentalActuationTasks()
        
        logging.info("Actuator location ID: %s", self.locationID)
    
    def _initEnvironmentalActuationTasks(self):
        """
        Initialize environmental actuation tasks based on configuration.
        """
        if not self.useEmulator:
            logging.info("ActuatorAdapterManager is using simulator tasks.")
            
            # Load the environmental tasks for simulated actuation
            self.humidifierActuator = HumidifierActuatorSimTask()
            self.hvacActuator = HvacActuatorSimTask()
            self.ledDisplayActuator = None  # No LED simulator in basic setup
        else:
            logging.info("ActuatorAdapterManager is using emulator tasks.")
            
            # Dynamically load humidifier emulator
            hueModule = import_module('programmingtheiot.cda.emulated.HumidifierEmulatorTask', 
                                     'HumidifierEmulatorTask')
            hueClazz = getattr(hueModule, 'HumidifierEmulatorTask')
            self.humidifierActuator = hueClazz()
            
            # Dynamically load HVAC emulator
            hveModule = import_module('programmingtheiot.cda.emulated.HvacEmulatorTask', 
                                     'HvacEmulatorTask')
            hveClazz = getattr(hveModule, 'HvacEmulatorTask')
            self.hvacActuator = hveClazz()
            
            # Dynamically load LED display emulator
            leModule = import_module('programmingtheiot.cda.emulated.LedDisplayEmulatorTask', 
                                    'LedDisplayEmulatorTask')
            leClazz = getattr(leModule, 'LedDisplayEmulatorTask')
            self.ledDisplayActuator = leClazz()

    def sendActuatorCommand(self, data: ActuatorData) -> bool:
        """
        Send actuator command to the appropriate actuator task.
        
        @param data The ActuatorData to process
        @return True if successful, False otherwise
        """
        if data and not data.isResponseFlagEnabled():
            if data.getLocationID() == self.locationID:
                logging.info('Processing actuator command for loc ID %s.', 
                           str(data.getLocationID()))
                
                aType = data.getTypeID()
                responseData = None
                
                if aType == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE and hasattr(self, 'humidifierActuator'):
                    responseData = self.humidifierActuator.updateActuator(data)
                    logging.debug("Humidifier actuator command processed")
                elif aType == ConfigConst.HVAC_ACTUATOR_TYPE and hasattr(self, 'hvacActuator'):
                    responseData = self.hvacActuator.updateActuator(data)
                    logging.debug("HVAC actuator command processed")
                elif aType == ConfigConst.LED_DISPLAY_ACTUATOR_TYPE and hasattr(self, 'ledDisplayActuator') and self.ledDisplayActuator:
                    responseData = self.ledDisplayActuator.updateActuator(data)
                    logging.debug("LED display actuator command processed")
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
        """
        Set the data message listener for callbacks.
        
        @param listener The IDataMessageListener instance
        @return True if successful, False otherwise
        """
        if listener:
            self.dataMsgListener = listener
            return True
        return False
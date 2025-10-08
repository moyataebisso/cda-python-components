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
from programmingtheiot.data.ActuatorData import ActuatorData

class BaseActuatorSimTask:
    """
    Base class for actuator simulation tasks.
    """
    
    def __init__(self, name = ConfigConst.NOT_SET, 
                 typeID = ConfigConst.DEFAULT_ACTUATOR_TYPE, 
                 simpleName = "Actuator"):
        """
        Constructor.
        """
        self.name = name
        self.typeID = typeID
        self.simpleName = simpleName
        self.lastKnownCommand = None
        self.lastKnownValue = None
    
    def updateActuator(self, data: ActuatorData) -> ActuatorData:
        """
        Update the actuator based on the command data.
        """
        if data and self.typeID == data.getTypeID():
            curCommand = data.getCommand()
            curVal = data.getValue()
            
            # Check for duplicate command
            if curCommand == self.lastKnownCommand and curVal == self.lastKnownValue:
                logging.debug("Ignoring repeated actuator command and value: %s %s",
                            str(curCommand), str(curVal))
                return None
            
            statusCode = ConfigConst.DEFAULT_STATUS
            
            if curCommand == ConfigConst.COMMAND_ON:
                logging.info("Activating actuator...")
                statusCode = self._activateActuator(data.getValue(), data.getStateData())
            elif curCommand == ConfigConst.COMMAND_OFF:
                logging.info("Deactivating actuator...")
                statusCode = self._deactivateActuator(data.getValue(), data.getStateData())
            else:
                logging.warning("Unknown actuator command: %s", str(curCommand))
                statusCode = -1
            
            # Update last known state
            self.lastKnownCommand = curCommand
            self.lastKnownValue = curVal
            
            # Create response
            responseData = ActuatorData(typeID=self.typeID, name=self.name)
            responseData.updateData(data)
            responseData.setStatusCode(statusCode)
            responseData.setAsResponse()
            
            return responseData
        
        return None
    
    def _activateActuator(self, val = ConfigConst.DEFAULT_VAL, stateData = None) -> int:
        """
        Activate the actuator (to be overridden by subclasses).
        """
        msg = "\n*******\n* O N *\n*******\n%s VALUE -> %.1f\n=======" % (self.simpleName, val)
        logging.info("Simulating %s actuator ON: %s", self.name, msg)
        return 0
    
    def _deactivateActuator(self, val = ConfigConst.DEFAULT_VAL, stateData = None) -> int:
        """
        Deactivate the actuator (to be overridden by subclasses).
        """
        msg = "\n*******\n* OFF *\n*******"
        logging.info("Simulating %s actuator OFF: %s", self.simpleName, msg)
        return 0
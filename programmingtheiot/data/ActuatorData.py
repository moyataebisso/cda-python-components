#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#
# Copyright (c) 2020 - 2025 by Andrew D. King
#

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.BaseIotData import BaseIotData

class ActuatorData(BaseIotData):
    """
    Container for actuator data and commands.
    """
    
    def __init__(self, typeID = ConfigConst.DEFAULT_ACTUATOR_TYPE, name = ConfigConst.NOT_SET, d = None):
        """
        Constructor.
        """
        super(ActuatorData, self).__init__(name=name, typeID=typeID, d=d)
        self.command = ConfigConst.DEFAULT_COMMAND
        self.value = ConfigConst.DEFAULT_VAL
        self.stateData = None
        self.isResponse = False
        
        if d:
            self.updateData(d)
    
    def getCommand(self):
        return self.command
    
    def getValue(self):
        return self.value
    
    def getStateData(self):
        return self.stateData
    
    def isResponseFlagEnabled(self):
        return self.isResponse
    
    def setAsResponse(self):
        self.isResponse = True
    
    def setCommand(self, command):
        self.command = command
    
    def setValue(self, val):
        self.value = val
    
    def setStateData(self, stateData):
        self.stateData = stateData
    
    def _handleUpdateData(self, data):
        """
        Handle update from another ActuatorData instance.
        """
        if data and isinstance(data, ActuatorData):
            self.command = data.getCommand()
            self.value = data.getValue()
            self.stateData = data.getStateData()
    
    def __str__(self):
        """
        String representation.
        """
        s = super().__str__()
        s = s + ",command=%d,value=%.4f,isResponse=%s" % (self.command, self.value, self.isResponse)
        if self.stateData:
            s = s + ",stateData=%s" % self.stateData
        return s
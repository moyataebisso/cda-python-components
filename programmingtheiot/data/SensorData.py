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

class SensorData(BaseIotData):
    """
    Container for sensor data, extending BaseIotData.
    """
    
    def __init__(self, typeID = ConfigConst.DEFAULT_SENSOR_TYPE, name = ConfigConst.NOT_SET, d = None):
        """
        Constructor.
        """
        super(SensorData, self).__init__(name=name, typeID=typeID, d=d)
        self.value = ConfigConst.DEFAULT_VAL
        
        if d:
            self.updateData(d)
    
    def getValue(self):
        """
        Get the sensor value.
        """
        return self.value
    
    def setValue(self, val):
        """
        Set the sensor value and update timestamp.
        """
        self.value = val
        self.updateTimeStamp()
    
    def _handleUpdateData(self, data):
        """
        Handle update from another SensorData instance.
        """
        if data and isinstance(data, SensorData):
            self.value = data.getValue()
    
    def __str__(self):
        """
        String representation.
        """
        s = super().__str__()
        s = s + ",value=%.4f" % (self.value)
        return s
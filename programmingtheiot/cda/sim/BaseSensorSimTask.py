#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#
# Copyright (c) 2020 - 2025 by Andrew D. King
#

import random
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataSet

class BaseSensorSimTask:
    """
    Base class for sensor simulation tasks.
    """
    
    DEFAULT_MIN_VAL = ConfigConst.DEFAULT_VAL
    DEFAULT_MAX_VAL = 100.0
    
    def __init__(self, name = ConfigConst.NOT_SET, typeID = ConfigConst.DEFAULT_SENSOR_TYPE,
                 dataSet = None, minVal = DEFAULT_MIN_VAL, maxVal = DEFAULT_MAX_VAL):
        """
        Constructor.
        """
        self.name = name
        self.typeID = typeID
        self.dataSet = dataSet
        self.dataSetIndex = 0
        self.minVal = minVal
        self.maxVal = maxVal
        self.latestSensorData = None
        self.useRandomizer = (dataSet is None)
    
    def generateTelemetry(self) -> SensorData:
        """
        Generate new sensor telemetry data.
        """
        self.latestSensorData = SensorData(typeID=self.typeID, name=self.name)
        
        if self.useRandomizer:
            sensorVal = random.uniform(self.minVal, self.maxVal)
        else:
            sensorVal = self.dataSet.getDataEntry(index=self.dataSetIndex)
            self.dataSetIndex += 1
            if self.dataSetIndex >= self.dataSet.getDataEntryCount():
                self.dataSetIndex = 0
        
        self.latestSensorData.setValue(sensorVal)
        return self.latestSensorData
    
    def getTelemetryValue(self) -> float:
        """
        Get the latest telemetry value.
        """
        if not self.latestSensorData:
            self.generateTelemetry()
        return self.latestSensorData.getValue()
    
    def getName(self):
        return self.name
    
    def getTypeID(self):
        return self.typeID
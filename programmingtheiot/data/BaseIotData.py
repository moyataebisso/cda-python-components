
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 - 2025 by Andrew D. King
# 

#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#
# Copyright (c) 2020 - 2025 by Andrew D. King
#

from datetime import datetime, timezone
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil

class BaseIotData(object):
    """
    This is the base class for all data containers. It stores values that each
    sub-class is expected to set and / or utilization, including the name,
    location ID, type ID, location specifics, and status information.
    """

    def __init__(self, name = ConfigConst.NOT_SET, typeID = ConfigConst.DEFAULT_TYPE_ID, d = None):
        """
        Constructor.
        @param d Defaults to None. The data (dict) to use for setting all parameters.
        """
        self.name = name
        self.typeID = typeID
        self.statusCode = ConfigConst.DEFAULT_STATUS
        self.hasError = False
        
        # Load locationID from config
        configUtil = ConfigUtil()
        self.locationID = configUtil.getProperty(
            section = ConfigConst.CONSTRAINED_DEVICE,
            key = ConfigConst.DEVICE_LOCATION_ID_KEY,
            defaultVal = ConfigConst.NOT_SET)
        
        # Initialize location data
        self.latitude = ConfigConst.DEFAULT_LAT
        self.longitude = ConfigConst.DEFAULT_LON
        self.elevation = ConfigConst.DEFAULT_ELEVATION
        
        # Initialize timestamp
        self.timeStamp = None
        self.updateTimeStamp()
        
        # If dict provided, update from it
        if d:
            self.updateData(d)
    
    def getName(self):
        return self.name
    
    def getLocationID(self):
        return self.locationID
    
    def getStatusCode(self):
        return self.statusCode
    
    def getTimeStamp(self):
        return self.timeStamp
    
    def getTypeID(self):
        return self.typeID
    
    def hasErrorFlag(self):
        return self.hasError
    
    def setLocationID(self, locationID):
        self.locationID = locationID
    
    def setName(self, name):
        self.name = name
    
    def setStatusCode(self, statusCode):
        self.statusCode = statusCode
        if statusCode < 0:
            self.hasError = True
        else:
            self.hasError = False
    
    def updateData(self, data):
        """
        Update this object from another BaseIotData instance or dict.
        """
        if data:
            if isinstance(data, BaseIotData):
                self.name = data.getName()
                self.typeID = data.getTypeID()
                self.statusCode = data.getStatusCode()
                self.locationID = data.getLocationID()
                self.latitude = data.latitude
                self.longitude = data.longitude
                self.elevation = data.elevation
                self.updateTimeStamp()
                self._handleUpdateData(data)
            elif isinstance(data, dict):
                # Handle dict update
                for key, value in data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
                self.updateTimeStamp()
    
    def updateTimeStamp(self):
        """
        Update the timestamp to current UTC time in ISO format.
        """
        self.timeStamp = datetime.now(timezone.utc).isoformat()
    
    def _handleUpdateData(self, data):
        """
        Template method for subclasses to override.
        """
        pass
    
    def __str__(self):
        """
        String representation of the object.
        """
        s = "name=%s,typeID=%d,timeStamp=%s,statusCode=%d,hasError=%s,locationID=%s," \
            "latitude=%.6f,longitude=%.6f,elevation=%.1f" % \
            (self.name, self.typeID, self.timeStamp, self.statusCode, self.hasError,
             self.locationID, self.latitude, self.longitude, self.elevation)
        return s

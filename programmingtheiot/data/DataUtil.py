#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#
# Copyright (c) 2020 by Andrew D. King
#

import json
import logging

from decimal import Decimal
from json import JSONEncoder

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DataUtil():
    """
    Data utility class for converting between data objects and JSON.
    """
    
    def __init__(self, encodeToUtf8=True):
        """
        Constructor
        
        @param encodeToUtf8 If true, encode to UTF-8; otherwise, use default encoding
        """
        self.encodeToUtf8 = encodeToUtf8
        
        logging.info("DataUtil initialized")
    
    def actuatorDataToJson(self, data: ActuatorData) -> str:
        """
        Convert ActuatorData to JSON string
        
        @param data The ActuatorData instance to convert
        @return JSON string representation
        """
        if not data:
            return None
            
        jsonData = self._generateJsonData(data)
        return jsonData
    
    def sensorDataToJson(self, data: SensorData) -> str:
        """
        Convert SensorData to JSON string
        
        @param data The SensorData instance to convert
        @return JSON string representation
        """
        if not data:
            return None
            
        jsonData = self._generateJsonData(data)
        return jsonData
    
    def systemPerformanceDataToJson(self, data: SystemPerformanceData) -> str:
        """
        Convert SystemPerformanceData to JSON string
        
        @param data The SystemPerformanceData instance to convert
        @return JSON string representation
        """
        if not data:
            return None
            
        jsonData = self._generateJsonData(data)
        return jsonData
    
    def jsonToActuatorData(self, jsonData: str) -> ActuatorData:
        """
        Convert JSON string to ActuatorData
        
        @param jsonData The JSON string to convert
        @return ActuatorData instance
        """
        if not jsonData:
            return None
            
        jsonStruct = json.loads(jsonData)
        
        # Create ActuatorData with typeID if present
        if 'typeID' in jsonStruct:
            ad = ActuatorData(typeID=jsonStruct['typeID'])
        else:
            ad = ActuatorData()
        
        # Set base fields
        if 'name' in jsonStruct:
            ad.setName(jsonStruct['name'])
        if 'locationID' in jsonStruct:
            ad.setLocationID(jsonStruct['locationID'])
        if 'statusCode' in jsonStruct:
            ad.setStatusCode(jsonStruct['statusCode'])
        
        # Directly set timestamp to preserve original value
        if 'timeStamp' in jsonStruct:
            ad.timeStamp = jsonStruct['timeStamp']
        
        # Set ActuatorData specific fields
        if 'command' in jsonStruct:
            ad.setCommand(jsonStruct['command'])
        if 'value' in jsonStruct:
            ad.setValue(jsonStruct['value'])
        if 'stateData' in jsonStruct:
            ad.setStateData(jsonStruct['stateData'])
        if 'isResponse' in jsonStruct and jsonStruct['isResponse']:
            ad.setAsResponse()
            
        return ad
    
    def jsonToSensorData(self, jsonData: str) -> SensorData:
        """
        Convert JSON string to SensorData
        
        @param jsonData The JSON string to convert
        @return SensorData instance
        """
        if not jsonData:
            return None
            
        jsonStruct = json.loads(jsonData)
        
        # Create SensorData with typeID if present
        if 'typeID' in jsonStruct:
            sd = SensorData(typeID=jsonStruct['typeID'])
        else:
            sd = SensorData()
        
        # IMPORTANT: Set timestamp BEFORE other fields to avoid it being overwritten
        # This is the key fix - some setters may update the timestamp
        if 'timeStamp' in jsonStruct:
            sd.timeStamp = jsonStruct['timeStamp']
        
        # Set base fields
        if 'name' in jsonStruct:
            sd.setName(jsonStruct['name'])
        if 'locationID' in jsonStruct:
            sd.setLocationID(jsonStruct['locationID'])
        if 'statusCode' in jsonStruct:
            sd.setStatusCode(jsonStruct['statusCode'])
        
        # Set SensorData specific fields
        if 'value' in jsonStruct:
            sd.setValue(jsonStruct['value'])
        
        # Set timestamp again in case it was overwritten
        if 'timeStamp' in jsonStruct:
            sd.timeStamp = jsonStruct['timeStamp']
            
        return sd
    
    def jsonToSystemPerformanceData(self, jsonData: str) -> SystemPerformanceData:
        """
        Convert JSON string to SystemPerformanceData
        
        @param jsonData The JSON string to convert
        @return SystemPerformanceData instance
        """
        if not jsonData:
            return None
            
        jsonStruct = json.loads(jsonData)
        
        spd = SystemPerformanceData()
        
        # Set base fields
        if 'name' in jsonStruct:
            spd.setName(jsonStruct['name'])
        if 'locationID' in jsonStruct:
            spd.setLocationID(jsonStruct['locationID'])
        if 'statusCode' in jsonStruct:
            spd.setStatusCode(jsonStruct['statusCode'])
        
        # Directly set timestamp to preserve original value
        if 'timeStamp' in jsonStruct:
            spd.timeStamp = jsonStruct['timeStamp']
        
        # Set SystemPerformanceData specific fields
        if 'cpuUtil' in jsonStruct:
            spd.setCpuUtilization(jsonStruct['cpuUtil'])
        if 'memUtil' in jsonStruct:
            spd.setMemoryUtilization(jsonStruct['memUtil'])
        if 'diskUtil' in jsonStruct:
            spd.setDiskUtilization(jsonStruct['diskUtil'])
            
        return spd
    
    def _generateJsonData(self, obj) -> str:
        """
        Generate JSON string from object
        
        @param obj The object to convert
        @return JSON string
        """
        jsonData = None
        
        if self.encodeToUtf8:
            jsonData = json.dumps(obj, cls=JsonDataEncoder, ensure_ascii=False).encode('utf-8')
            jsonData = jsonData.decode('utf-8')
        else:
            jsonData = json.dumps(obj, cls=JsonDataEncoder)
            
        return jsonData

class JsonDataEncoder(JSONEncoder):
    """
    Custom JSON encoder to handle object serialization
    """
    
    def default(self, obj):
        """
        Handle encoding of custom objects
        
        @param obj The object to encode
        @return Dictionary representation of object
        """
        if isinstance(obj, (ActuatorData, SensorData, SystemPerformanceData)):
            return obj.__dict__
            
        if isinstance(obj, Decimal):
            return float(obj)
            
        return JSONEncoder.default(self, obj)
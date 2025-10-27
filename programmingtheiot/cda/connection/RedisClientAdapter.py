import redis
import json
import logging
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData

class RedisClientAdapter:
    def __init__(self, host='localhost', port=6379, db=0):
        """Initialize Redis client"""
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.dataUtil = DataUtil()
        logging.info("Redis client initialized - host: %s, port: %d", host, port)
    
    def storeActuatorData(self, data: ActuatorData) -> bool:
        """Store ActuatorData in Redis"""
        try:
            jsonData = self.dataUtil.actuatorDataToJson(data)
            self.client.lpush("ActuatorData", jsonData)
            logging.debug("Stored ActuatorData in Redis")
            return True
        except Exception as e:
            logging.error("Failed to store ActuatorData: %s", str(e))
            return False
    
    def storeSensorData(self, data: SensorData) -> bool:
        """Store SensorData in Redis"""
        try:
            jsonData = self.dataUtil.sensorDataToJson(data)
            self.client.lpush("SensorData", jsonData)
            logging.debug("Stored SensorData in Redis")
            return True
        except Exception as e:
            logging.error("Failed to store SensorData: %s", str(e))
            return False
    
    def getActuatorData(self) -> list:
        """Get all ActuatorData from Redis"""
        try:
            jsonList = self.client.lrange("ActuatorData", 0, -1)
            return [self.dataUtil.jsonToActuatorData(json) for json in jsonList]
        except Exception as e:
            logging.error("Failed to get ActuatorData: %s", str(e))
            return []

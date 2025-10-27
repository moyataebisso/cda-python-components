import unittest
import logging
from programmingtheiot.cda.connection.RedisClientAdapter import RedisClientAdapter
from programmingtheiot.data.ActuatorData import ActuatorData

class RedisClientAdapterTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)
        logging.info("Setting up RedisClientAdapterTest")
        cls.redisAdapter = RedisClientAdapter()
    
    def test_StoreAndRetrieveActuatorData(self):
        """Test storing and retrieving ActuatorData"""
        logging.info("Testing Redis storage")
        
        # Create test data
        actuatorData = ActuatorData()
        actuatorData.setName("TestActuator")
        actuatorData.setCommand(1)
        actuatorData.setValue(25.5)
        actuatorData.setLocationID("constraineddevice001")
        
        # Store in Redis
        result = self.redisAdapter.storeActuatorData(actuatorData)
        self.assertTrue(result)
        
        logging.info("Stored ActuatorData successfully in Redis")

if __name__ == '__main__':
    unittest.main()

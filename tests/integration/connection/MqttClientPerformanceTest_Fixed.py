import logging
import unittest
import time

from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.SensorData import SensorData

class MqttClientPerformanceTest(unittest.TestCase):
    NS_IN_MILLIS = 1000000
    MAX_TEST_RUNS = 10000
    
    @classmethod
    def setUpClass(self):
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        
    def setUp(self):
        self.mqttClient = MqttClientConnector(clientID = 'CDAMqttClientPerformanceTest001', enablePerformanceTest = True)

    def tearDown(self):
        pass

    def testConnectAndDisconnect(self):
        startTime = time.time_ns()
        
        self.assertTrue(self.mqttClient.connectClient())
        time.sleep(0.5)  # Allow connection to complete
        self.assertTrue(self.mqttClient.disconnectClient())
        
        endTime = time.time_ns()
        elapsedMillis = (endTime - startTime) / self.NS_IN_MILLIS
        
        logging.info("Connect and Disconnect: " + str(elapsedMillis) + " ms")
        
    def testPublishQoS0(self):
        self._execTestPublish(self.MAX_TEST_RUNS, 0)

    def testPublishQoS1(self):
        self._execTestPublish(self.MAX_TEST_RUNS, 1)

    def testPublishQoS2(self):
        self._execTestPublish(self.MAX_TEST_RUNS, 2)

    def _execTestPublish(self, maxTestRuns: int, qos: int):
        self.assertTrue(self.mqttClient.connectClient())
        time.sleep(1)
        
        sensorData = SensorData()
        payload = DataUtil().sensorDataToJson(sensorData)
        
        startTime = time.time_ns()
        
        for seqNo in range(0, maxTestRuns):
            self.mqttClient.publishMessage(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, msg = payload, qos = qos)
            
        endTime = time.time_ns()
        elapsedMillis = (endTime - startTime) / self.NS_IN_MILLIS
        
        self.assertTrue(self.mqttClient.disconnectClient())
        
        logging.info("Publish message - QoS " + str(qos) + " [" + str(maxTestRuns) + "]: " + str(elapsedMillis) + " ms")

if __name__ == '__main__':
    unittest.main()

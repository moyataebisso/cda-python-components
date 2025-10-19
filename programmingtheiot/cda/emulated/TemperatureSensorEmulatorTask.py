from programmingtheiot.data.SensorData import SensorData
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from pisense import SenseHAT

import logging

class TemperatureSensorEmulatorTask(BaseSensorSimTask):
    def __init__(self):
        super(TemperatureSensorEmulatorTask, self).__init__(
            name=ConfigConst.TEMP_SENSOR_NAME,
            typeID=ConfigConst.TEMP_SENSOR_TYPE)
        
        enableEmulation = ConfigUtil().getBoolean(
            ConfigConst.CONSTRAINED_DEVICE, 
            ConfigConst.ENABLE_EMULATOR_KEY)
        
        self.sh = SenseHAT(emulate=enableEmulation)
        logging.info(f"TemperatureSensorEmulatorTask initialized with emulation={enableEmulation}")
    
    def generateTelemetry(self) -> SensorData:
        sensorData = SensorData(name=self.getName(), typeID=self.getTypeID())
        
        try:
            sensorVal = self.sh.environ.temperature
        except:
            # Fallback to simulated value
            sensorVal = 20.0
            
        sensorData.setValue(sensorVal)
        self.latestSensorData = sensorData
        return sensorData
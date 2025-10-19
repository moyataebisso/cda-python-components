from programmingtheiot.data.SensorData import SensorData
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from pisense import SenseHAT

import logging

class PressureSensorEmulatorTask(BaseSensorSimTask):
    def __init__(self):
        super(PressureSensorEmulatorTask, self).__init__(
            name=ConfigConst.PRESSURE_SENSOR_NAME,
            typeID=ConfigConst.PRESSURE_SENSOR_TYPE)
        
        enableEmulation = ConfigUtil().getBoolean(
            ConfigConst.CONSTRAINED_DEVICE, 
            ConfigConst.ENABLE_EMULATOR_KEY)
        
        self.sh = SenseHAT(emulate=enableEmulation)
        logging.info(f"PressureSensorEmulatorTask initialized with emulation={enableEmulation}")
    
    def generateTelemetry(self) -> SensorData:
        sensorData = SensorData(name=self.getName(), typeID=self.getTypeID())
        
        try:
            sensorVal = self.sh.environ.pressure
        except:
            # Fallback to simulated value
            sensorVal = 1013.25
            
        sensorData.setValue(sensorVal)
        self.latestSensorData = sensorData
        return sensorData
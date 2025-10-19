import logging
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask
from pisense import SenseHAT

class LedDisplayEmulatorTask(BaseActuatorSimTask):
    def __init__(self):
        super(LedDisplayEmulatorTask, self).__init__(
            name=ConfigConst.LED_ACTUATOR_NAME,
            typeID=ConfigConst.LED_DISPLAY_ACTUATOR_TYPE,
            simpleName="LED_Display")
        
        enableEmulation = ConfigUtil().getBoolean(
            ConfigConst.CONSTRAINED_DEVICE, 
            ConfigConst.ENABLE_EMULATOR_KEY)
        
        self.sh = SenseHAT(emulate=enableEmulation)
        logging.info(f"LedDisplayEmulatorTask initialized with emulation={enableEmulation}")
    
    def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, 
                          stateData: str = None) -> int:
        try:
            if self.sh.screen:
                self.sh.screen.scroll_text(stateData if stateData else "LED ON", size=8)
                return 0
        except:
            logging.info(f"Emulator: LED Display showing: {stateData if stateData else 'LED ON'}")
            return 0
            
        logging.warning("No SenseHAT LED screen instance to write.")
        return -1
    
    def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, 
                            stateData: str = None) -> int:
        try:
            if self.sh.screen:
                self.sh.screen.clear()
                return 0
        except:
            logging.info("Emulator: LED Display cleared")
            return 0
            
        logging.warning("No SenseHAT LED screen instance to clear.")
        return -1
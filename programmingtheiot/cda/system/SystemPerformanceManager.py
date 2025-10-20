import logging
from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask

# Add this import
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class SystemPerformanceManager(object):
    
    def __init__(self):
        configUtil = ConfigUtil()
        
        self.pollRate = configUtil.getInteger(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.POLL_CYCLES_KEY,
            defaultVal=ConfigConst.DEFAULT_POLL_CYCLES)
        
        self.locationID = configUtil.getProperty(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.DEVICE_LOCATION_ID_KEY,
            defaultVal=ConfigConst.NOT_SET)
        
        if self.pollRate <= 0:
            self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
            
        self.dataMsgListener = None
        
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.handleTelemetry, 'interval', seconds=self.pollRate)
        
        self.cpuUtilTask = SystemCpuUtilTask()
        self.memUtilTask = SystemMemUtilTask()
        
        logging.info("System Performance Manager initialized with poll rate: %s", self.pollRate)
    
    def handleTelemetry(self):
        """
        Handle telemetry using SystemPerformanceData container
        """
        # Get CPU utilization
        cpuUtil = self.cpuUtilTask.getTelemetryValue()
        
        # Get Memory utilization
        memUtil = self.memUtilTask.getTelemetryValue()
        
        # Create SystemPerformanceData container
        sysPerfData = SystemPerformanceData()
        sysPerfData.setLocationID(self.locationID)
        sysPerfData.setCpuUtilization(cpuUtil)
        sysPerfData.setMemoryUtilization(memUtil)
        
        # Log the data
        logging.debug('CPU utilization: %s%%', cpuUtil)
        logging.debug('Memory utilization: %s%%', memUtil)
        logging.info('System performance data: %s', str(sysPerfData))
        
        # Send to listener if available
        if self.dataMsgListener:
            self.dataMsgListener.handleSystemPerformanceMessage(sysPerfData)
    
    def setDataMessageListener(self, listener: IDataMessageListener):
        if listener:
            self.dataMsgListener = listener
    
    def startManager(self):
        logging.info("Starting SystemPerformanceManager...")
        
        if not self.scheduler.running:
            self.scheduler.start()
            logging.info("SystemPerformanceManager started.")
        else:
            logging.warning("SystemPerformanceManager scheduler already running.")
    
    def stopManager(self):
        logging.info("Stopping SystemPerformanceManager...")
        
        try:
            self.scheduler.shutdown()
            logging.info("SystemPerformanceManager stopped.")
        except:
            logging.warning("SystemPerformanceManager scheduler already stopped.")
#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#

import logging
from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class SystemPerformanceManager(object):
    """
    System performance manager implementation.
    """
    
    def __init__(self):
        configUtil = ConfigUtil()
        
        self.pollRate = configUtil.getInteger(
            section = ConfigConst.CONSTRAINED_DEVICE,
            key = ConfigConst.POLL_CYCLES_KEY,
            defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)
        
        if self.pollRate <= 0:
            self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
            
        self.dataMsgListener = None
        
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.handleTelemetry, 'interval', seconds = self.pollRate)
        
        self.cpuUtilTask = SystemCpuUtilTask()
        self.memUtilTask = SystemMemUtilTask()
        
        logging.info("Initialized SystemPerformanceManager with poll rate: %s", self.pollRate)
    
    def handleTelemetry(self):
        cpuVal = self.cpuUtilTask.getTelemetryValue()
        memVal = self.memUtilTask.getTelemetryValue()
        
        sysPerfData = SystemPerformanceData()
        sysPerfData.setCpuUtilization(cpuVal)
        sysPerfData.setMemoryUtilization(memVal)
        
        logging.debug('CPU utilization: %s%%', cpuVal)
        logging.debug('Memory utilization: %s%%', memVal)
        
        if self.dataMsgListener:
            self.dataMsgListener.handleSystemPerformanceMessage(sysPerfData)
    
    def setDataMessageListener(self, listener: IDataMessageListener):
        if listener:
            self.dataMsgListener = listener
    
    def startManager(self):
        logging.info("Starting SystemPerformanceManager...")
        
        if not self.scheduler.running:
            self.scheduler.start()
        else:
            logging.warning("SystemPerformanceManager scheduler already started.")
    
    def stopManager(self):
        logging.info("Stopping SystemPerformanceManager...")
        
        try:
            self.scheduler.shutdown()
        except:
            logging.warning("SystemPerformanceManager scheduler already stopped.")
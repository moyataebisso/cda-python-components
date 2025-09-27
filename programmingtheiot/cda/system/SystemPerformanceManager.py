import logging
from apscheduler.schedulers.background import BackgroundScheduler

from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask

class SystemPerformanceManager:
    def __init__(self):
        logging.info("Initializing SystemPerformanceManager...")
        self.scheduler = BackgroundScheduler()
        self.cpuUtilTask = SystemCpuUtilTask()
        self.memUtilTask = SystemMemUtilTask()
        self.pollRate = 30  # seconds
        
    def startManager(self):
        logging.info("Starting SystemPerformanceManager...")
        self.scheduler.add_job(
            self._handleTelemetry,
            'interval',
            seconds=self.pollRate
        )
        self.scheduler.start()
        
    def stopManager(self):
        logging.info("Stopping SystemPerformanceManager...")
        self.scheduler.shutdown()
        
    def _handleTelemetry(self):
        cpuUtil = self.cpuUtilTask.getTelemetryValue()
        memUtil = self.memUtilTask.getTelemetryValue()
        
        logging.info(f"CPU Utilization: {cpuUtil}%")
        logging.info(f"Memory Utilization: {memUtil}%")

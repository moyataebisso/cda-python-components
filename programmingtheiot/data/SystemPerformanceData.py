#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#
# Copyright (c) 2020 - 2025 by Andrew D. King
#

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.BaseIotData import BaseIotData

class SystemPerformanceData(BaseIotData):
    """
    Container for system performance metrics.
    """
    
    def __init__(self, d = None):
        """
        Constructor.
        """
        super(SystemPerformanceData, self).__init__(
            name=ConfigConst.SYSTEM_PERF_NAME,
            typeID=ConfigConst.SYSTEM_PERF_TYPE,
            d=d)
        
        self.cpuUtil = ConfigConst.DEFAULT_VAL
        self.memUtil = ConfigConst.DEFAULT_VAL
        
        if d:
            self.updateData(d)
    
    def getCpuUtilization(self):
        return self.cpuUtil
    
    def getMemoryUtilization(self):
        return self.memUtil
    
    def setCpuUtilization(self, cpuUtil):
        self.cpuUtil = cpuUtil
    
    def setMemoryUtilization(self, memUtil):
        self.memUtil = memUtil
    
    def _handleUpdateData(self, data):
        """
        Handle update from another SystemPerformanceData instance.
        """
        if data and isinstance(data, SystemPerformanceData):
            self.cpuUtil = data.getCpuUtilization()
            self.memUtil = data.getMemoryUtilization()
    
    def __str__(self):
        """
        String representation.
        """
        s = super().__str__()
        s = s + ",cpuUtil=%.2f,memUtil=%.2f" % (self.cpuUtil, self.memUtil)
        return s
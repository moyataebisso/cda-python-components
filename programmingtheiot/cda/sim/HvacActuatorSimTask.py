#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#
# Copyright (c) 2020 - 2025 by Andrew D. King
#

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

class HvacActuatorSimTask(BaseActuatorSimTask):
    """
    HVAC actuator simulator task.
    """
    
    def __init__(self):
        """
        Constructor.
        """
        super(HvacActuatorSimTask, self).__init__(
            name = ConfigConst.HVAC_ACTUATOR_NAME,
            typeID = ConfigConst.HVAC_ACTUATOR_TYPE,
            simpleName = "HVAC")
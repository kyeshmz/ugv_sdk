import ugv_sdk_py
from ugv_sdk_py import hunter_robot, ranger_robot, scout_robot

scout_robot.ScoutRobot(ugv_sdk_py.ProtocolVersion.AGX_V2, False)
hunter_robot.HunterRobot
ranger_robot.RangerRobot
print("ugv_sdk_py imported OK")

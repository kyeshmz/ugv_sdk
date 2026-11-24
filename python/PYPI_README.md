# ugv_sdk_py

Python bindings for [ugv_sdk](https://github.com/westonrobot/ugv_sdk), the C++ SDK
for mobile robot platforms by [Weston Robot](https://www.westonrobot.com/) and
[AgileX Robotics](http://www.agilex.ai/). It covers Scout, Hunter, Bunker,
Tracer and Ranger bases over CAN.

The SDK and the Python bindings are the work of Weston Robot and AgileX Robotics:

- Copyright (c) 2020-2024 Weston Robot
- Copyright (c) 2020-2024 AgileX Robotics

This is an unofficial build. Weston Robot and AgileX Robotics do not publish or
maintain it. The wheels are built from the fork at
[kyeshmz/ugv_sdk](https://github.com/kyeshmz/ugv_sdk). The fork changes only
packaging and CI, so it can ship prebuilt Linux wheels. The wheels follow
upstream's support matrix: Ubuntu 18.04, 20.04 and 22.04 (24.04 also works) on
x86_64 and arm64, and Python 3.8 or newer.
Report SDK bugs and robot support questions
[upstream](https://github.com/westonrobot/ugv_sdk/issues).

## Install

```
pip install ugv-sdk-py
```

## Usage

Bring up the CAN interface first (see the upstream README), then:

```python
import ugv_sdk_py
from ugv_sdk_py import scout_robot

robot = scout_robot.ScoutRobot(ugv_sdk_py.ProtocolVersion.AGX_V2, False)
robot.connect("can0")
robot.enable_commanded_mode()
robot.set_motion_command(0.0, 0.0)
print(robot.get_robot_state().motion_state.linear_velocity)
```

## License

Apache-2.0, the same as upstream. See `LICENSE`.

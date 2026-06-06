# mock_robot

[ROS](https://docs.ros.org) driver for Mock Robot using Roomba 694 based on iRobot Create 2.

## Origin

This package provides a simulation infrastructure for a Roomba-based MockBot. It has borrowed from the following repositories:
* Autonomy Labs create_robot https://github.com/AutonomyLab/create_robot
* iRobot Create 3 simulation https://github.com/iRobotEducation/create3_sim
* ROS naviation tutorial https://github.com/ros-navigation/navigation2_tutorials/tree/rolling/sam_bot_description

The design is from Camp Peavy's book on MockBots "The MockBOT: Over-the-shoulder instructions on how to build your own personal robot."
My contribution is to provide a simulated version of the Roomba-based MockBot using ROS2 Jazzy and Gazebo Harmonic.
Currently only teleoperation is possible. Future work will provide camera and navigation support.

## Install

#### Prerequisites

* [ROS 2](https://index.ros.org/doc/ros2/Installation)

Gazebo Harmonic:

sudo apt-get install ros-jazzy-ros-gz


#### Compiling

1. Create a colcon workspace
    ``` bash
    $ cd ~
    $ mkdir -p ros_ws/src
    $ cd ros_ws
    ```

2. Clone this repo
    ``` bash
    $ cd ~/ros_ws/src
    $ git clone https://github.com/Caprica666/mock_robot.git
    $ git clone https://github.com/AutonomyLab/libcreate.git
    ```

3. Install dependencies
    ``` bash
    $ cd ~/ros_ws
    $ rosdep update
    $ rosdep install --from-paths src -i
    ```

4. Build
    ``` bash
    $ cd ~/ros_ws
    $ colcon build
    ```
#### USB Permissions
5. In order to connect to the Mockbot over USB, ensure your user is in the dialout group
    ``` bash
    $ sudo usermod -a -G dialout $USER
    ```

6. Logout and login for permission to take effect

## Running the driver

### Setup

1. After compiling from source, don't forget to source your workspace:
    ``` bash
    $ source ~/ros_ws/install/setup.bash
    ```

2. Launch the existing launch file or adapt them to create your own.

### Launch file

To launch the MockBot without simulation:
``` bash
$ ros2 launch mock_bringup mockbot.launch.py
```

To launch the MockBot with Gazebo and RViz:
``` bash
$ ros2 launch mock_bringup mockbot_sim.launch.py
```

### Publishers

 Topic       | Description  | Type
-------------|--------------|------
 `joint_states` | The states (position, velocity) of the drive wheel joints | [sensor_msgs/msg/JointState][jointstate_msg]
 `/tf` | The transform from the `odom` frame to `base_footprint`. Only if the parameter `publish_tf` is `true` | [tf2_msgs/msg/TFMessage](https://docs.ros2.org/jazzy/api/tf2_msgs/msg/TFMessage.html)


### Subscribers

Topic       | Description   | Type
------------|---------------|------
`cmd_vel` | Drives the robot's wheels according to a forward and angular velocity | [geometry_msgs/msg/Twist][twist]

## Commanding your Create

You can move the robot around by sending [geometry_msgs/msg/Twist][twist] messages to the topic `cmd_vel`:

```
linear.x  (+)     Move forward (m/s)
          (-)     Move backward (m/s)
angular.z (+)     Rotate counter-clockwise (rad/s)
          (-)     Rotate clockwise (rad/s)
```
#### Velocity limits

` -0.5 <= linear.x <= 0.5` and `-4.25 <= angular.z <= 4.25`

### Teleoperation

`mock_bringup` comes with a launch file for teleoperating Create with a joystick.

``` bash
$ ros2 launch mock_bringup teleop.launch.py
```

### Contributors

[libcreate]:  https://github.com/AutonomyLab/libcreate
[create_msgs]:  http://github.com/autonomylab/create_robot/tree/foxy

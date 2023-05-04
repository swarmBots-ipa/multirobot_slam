#! /usr/bin/env python3

from multirobot_slam.multirobot_slam.multirobot_slam.multirobot_navigator import RobotNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
import rclpy
from rclpy.duration import Duration
from ament_index_python.packages import get_package_share_directory


def main(args=None):
    rclpy.init()

    namespace = 'agent_1'
    navigator = RobotNavigator(namespace)
    navigator.waitUntilNav2Active()

    if navigator.initial_pose_received:
        initial_pose = navigator.initial_pose

    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose.pose.position.x = 3.02
    goal_pose.pose.position.y = 4.11
    goal_pose.pose.orientation.z = 0.0
    goal_pose.pose.orientation.w = 1.0
    navigator.goToPose(goal_pose)


    i = 0
    while not navigator.isTaskComplete():
        i = i + 1
        feedback = navigator.getFeedback()
        if feedback and i % 5 == 0:
            print('Estimated time of arrival: ' + '{0:.0f}'.format(
                  Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9)
                  + ' seconds.')

    # Do something depending on the return code
    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Goal succeeded!')
    elif result == TaskResult.CANCELED:
        print('Goal was canceled!')
    elif result == TaskResult.FAILED:
        print('Goal failed!')
    else:
        print('Goal has an invalid return status!')

    #navigator.lifecycleShutdown()

    exit(0)

if __name__ == '__main__':
    main()

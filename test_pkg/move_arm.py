import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

from builtin_interfaces.msg import Duration


class MoveArm(Node):

    def __init__(self):
        super().__init__('move_arm')

        self.client = ActionClient(
            self,
            FollowJointTrajectory,
            '/crane_plus_arm_controller/follow_joint_trajectory'
        )

        self.get_logger().info("Waiting for action server...")
        self.client.wait_for_server()

        self.send_goal()

    def send_goal(self):

        goal_msg = FollowJointTrajectory.Goal()

        traj = JointTrajectory()

        traj.joint_names = [
            'crane_plus_joint1',
            'crane_plus_joint2',
            'crane_plus_joint3',
            'crane_plus_joint4'
        ]

        point = JointTrajectoryPoint()

        point.positions = [
            0.5,
            0.0,
            0.0,
            0.0
        ]

        point.time_from_start = Duration(
            sec=3,
            nanosec=0
        )

        traj.points.append(point)

        goal_msg.trajectory = traj

        self.get_logger().info("Sending goal...")

        self.client.send_goal_async(goal_msg)


def main(args=None):

    rclpy.init(args=args)

    node = MoveArm()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

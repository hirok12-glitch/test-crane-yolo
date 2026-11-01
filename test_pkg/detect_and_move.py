import sys

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

from builtin_interfaces.msg import Duration

from ultralytics import YOLO

class DetectAndMove(Node):

    def __init__(self, image_path):
        super().__init__('detect_and_move')

        self.image_path = image_path

        self.client = ActionClient(
            self,
            FollowJointTrajectory,
            '/crane_plus_arm_controller/follow_joint_trajectory'
        )

        self.get_logger().info("Waiting for action server...")
        self.client.wait_for_server()

        self.detect_and_move()

    def detect_and_move(self):

        model = YOLO("yolov8n.pt")

        results = model(self.image_path)

        detected = None

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                detected = model.names[cls]
                break

            if detected:
                break

        print(f"Detected: {detected}")

        if detected == "bottle":
            target = 0.5
            print("Bottle detected -> move left")

        elif detected == "car":
            target = -0.5
            print("Car detected -> move right")

        else:
            target = 0.0
            print("Unknown object")

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
            target,
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

        self.client.send_goal_async(goal_msg)


def main(args=None):

    rclpy.init(args=args)

    if len(sys.argv) != 2:
        print("usage:")
        print("ros2 run test_pkg detect_and_move IMAGE_PATH")
        return

    image_path = sys.argv[1]

    node = DetectAndMove(image_path)

    rclpy.spin_once(node, timeout_sec=5)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

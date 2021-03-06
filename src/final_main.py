#!/usr/bin/env python

import rospy
from final_a_star import floodFill, graphDataStructure
from std_msgs.msg import Header, String
from geometry_msgs.msg import Pose, PoseStamped, Point, PointStamped
import tf2_geometry_msgs
import tf2_ros


class MainRun:
    def __init__(self):
        self.fill = floodFill()
	self.tf_buffer = tf2_ros.Buffer()
        self.data_struc = graphDataStructure()
        # self.next_point = tuple(graphDataStructure().find_next_point(self.fill))
        self.next_point = self.data_struc.find_next_point(self.fill)
        self.robot_loc_x = 0
        self.robot_loc_y = 0
        self.did_send = False  # flag_from_ros
        self.target_pub = rospy.Publisher('/Current_Target', Pose, queue_size=10)
        #print('passed current target line')
        self.pos_sub = rospy.Subscriber('/map_odom', Pose, self.main_run_func)


    def main_run_func(self, pos_msg_m):
	self.target_pose = Pose()
	x = self.next_point[0]
        y = self.next_point[1]
	self.target_pose.position.x = self.map_range(self.next_point[0],0,384,-10,10)
	self.target_pose.position.y = self.map_range(self.next_point[1],0,384,-10,10)
	self.current_pos_interpret(pos_msg_m)
        current_time = rospy.get_rostime()

        limit = 10
        
        diff_x = abs(x - self.robot_loc_x)
        diff_y = abs(y - self.robot_loc_y)

        self.publish_target()

        # if self.did_send == True:
        #     beg_time = rospy.get_rostime()  # at this point the robot should begin it's move.
        #     self.did_send = False

        #time_taken = current_time - beg_time
        # print('time: ', time_taken)
        # print('what')
        # if time_taken > time_limit:
        #
        #     if diff_x > limit and diff_y > limit:
        #         print("robot didn't reach point")
        #         beg_time = current_time
        #         self.target_pub.publish(String(str(self.next_point)))
        #     # print("target published!")  # This should change based on the new explored map
        #
        # elif diff_x <= limit and diff_y <= limit:
        #     beg_time = current_time
        #     self.target_pub.publish(String(str(self.next_point)))
        #     # print("target published!")


    def publish_target(self):
        #print("target published!")
	self.target_pub.publish(self.target_pose)

    def current_pos_interpret(self, pos_msg):
        self.robot_loc_x = pos_msg.position.x
        self.robot_loc_y = pos_msg.position.y
	#print([self.robot_loc_x, self.robot_loc_y])

    def map_range(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


if __name__ == '__main__':
    time_limit = rospy.Duration(2)  # Time allowed for robot to reach destination in ms?
    beg_time = rospy.Duration(0)
    # current_time = 0

    rospy.init_node('final_main')

    # rate = rospy.Rate(1)
    # rate.sleep()
    pllanning = MainRun()
    #pllanning.main_run_func(time_limit, beg_time)
    rospy.spin()
    # print(newpoint.is_bot_at_endpoint(time_limit,beg_time,current_time))

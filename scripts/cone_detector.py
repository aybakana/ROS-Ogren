#!/usr/bin/python
import rospy
import numpy as np 
from operator import itemgetter
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PointStamped 
from geometry_msgs.msg import Point
from std_msgs.msg import Float32
from std_msgs.msg import Float64
import threading

class ConeDetector:

    def __init__(self):
        self.cone_sub = rospy.Subscriber("cone_location", Float32, self.phi_callback)
        self.scan_window=rospy.Publisher("laser_window", LaserScan, queue_size=4)
        self.cd_sub = rospy.Subscriber("scan", LaserScan, self.laser_callback)
        self.cd_pub = rospy.Publisher("cone_position", PointStamped, queue_size=4)

        self.phi = 90
        self.stampedpoint=PointStamped()
        self.counter=0
        self.lock = threading.Lock()

    def phi_callback(self, msg):
        with self.lock:
            self.phi =+ msg.data


    def laser_callback(self,msg):
        with self.lock:
            phi = self.phi

        time=rospy.Time.now()
        if abs(phi) <= 1:
            if phi > 0:
                phi *= 1.7
            else:
                phi *= 1.4
            phi_start = phi - .07
            phi_end = phi + .07

            start_point=int((msg.angle_max+phi_start)/(msg.angle_max-msg.angle_min)*len(msg.ranges))
            end_point=int((msg.angle_max+phi_end)/(msg.angle_max-msg.angle_min)*len(msg.ranges))


            scan = LaserScan()
            scan = msg
            scan.angle_min=phi_start
            scan.angle_max=phi_end
            scan.ranges = msg.ranges[start_point:end_point]
            point_list = scan.ranges
            self.scan_window.publish(scan)

            ranges = scan.ranges

            #find min range
            #extend k nearest of x in ranges for some constant k
            #if neighbors > 3 return mean([x, [neighbors of x]])
            #else x = next and repeat


            point_list = np.array(point_list)
            point_list[point_list > 4] = -1

            point_list = [i for i in point_list if i != -1]
            point = Point()
            point.x=np.mean(point_list)


            point.y=point.x*np.sin(phi)
            point.z=0.0

            if not abs(point.y) <= 3 and not abs(point.x) <= 5:
                return;

            self.counter+=1
            self.stampedpoint.header.seq=self.counter
            self.stampedpoint.header.frame_id="base_link"
            self.stampedpoint.header.stamp=time
            self.stampedpoint.point=point
            self.cd_pub.publish(self.stampedpoint)
        else:
            scan = LaserScan()
            scan = msg
            scan.ranges = []
            self.scan_window.publish(scan)

            point=Point()
            point.x=0.0
            point.y=0.0
            point.z=0.0
            self.counter+=1
            self.stampedpoint.header.seq=self.counter
            self.stampedpoint.header.frame_id="base_link"
            self.stampedpoint.header.stamp=time
            self.stampedpoint.point=point
            self.cd_pub.publish(self.stampedpoint)
            

if __name__=="__main__":
    rospy.init_node("ConeDetector")
    node=ConeDetector()
    rospy.spin()


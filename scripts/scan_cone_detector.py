#!/usr/bin/python
import rospy
import numpy as np 
from operator import itemgetter
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PointStamped 
from geometry_msgs.msg import Point
from std_msgs.msg import Float32
from std_msgs.msg import Float64

import tf
class ConeDetector:

    def __init__(self):
        #self.cone_sub = rospy.Subscriber("cone_location", Float32, self.phi_callback)
        self.scan_window=rospy.Publisher("laser_window", LaserScan, queue_size=4)
        self.cd_sub = rospy.Subscriber("scan", LaserScan, self.laser_callback)
        self.cd_pub = rospy.Publisher("cone_position", PointStamped, queue_size=4)
        self.phi = 0.2
        self.phi_start=self.phi
        self.phi_end = self.phi
        self.window=3
        self.stampedpoint=PointStamped()
        self.counter=0
        self.listener = tf.TransformListener(True, rospy.Duration(10.0))

    def phi_callback(self, msg):
        #print "recieved phi"
        self.phi=-msg.data
    def laser_callback(self,msg):
        #ang="resolution:%s"%str(msg.angle_max-msg.angle_min)

        # print "converting from %s to base_link" % msg.header.frame_id
        # msg.header.stamp = self.listener.getLatestCommonTime("/base_link",msg.header.frame_id)
        # msg = self.listener.transformScan("/base_link", msg)

        time=rospy.Time.now()
        if self.phi<np.pi:#check the angle
            phi_index=int((msg.angle_max+self.phi)/(msg.angle_max-msg.angle_min)*len(msg.ranges))
            phi_point=int((msg.angle_max+self.phi)/(msg.angle_max-msg.angle_min)*len(msg.ranges))
            points=msg.ranges[phi_index-10*self.window:phi_index+10*self.window]
            # # for i in range(phi_point-20*self.window,phi_point-20*self.window):
            # # 	mean=np.mean(msg.ranges[i-2:i+3])
            # # 	points.append((i,mean))

            distance = np.mean(points)
            # self.phi_start=self.phi-np.pi/(18+3*distance)
            # self.phi_end=self.phi+np.pi/(18+3*distance)
            self.phi_start=self.phi-.15
            self.phi_end=self.phi+.15
            start_point=int((msg.angle_max+self.phi_start)/(msg.angle_max-msg.angle_min)*len(msg.ranges))
            end_point=int((msg.angle_max+self.phi_end)/(msg.angle_max-msg.angle_min)*len(msg.ranges))
            #ang="start_point, end_point:%s"%str((start_point,end_point))
            #print ang
            #rospy.loginfo(ang)
            points=[]
            for i in range(start_point, end_point-5):
                wind=msg.ranges[i:i+6]
                mean=np.mean(wind)
                points.append((i+2,mean))
            point = min(points,key=lambda item:item[1])
            position = start_point+point[0]
            dist=point[1]
            angle=msg.angle_increment*position+msg.angle_min
            x=dist*np.sin(angle)
            y=dist*np.cos(angle)
            point = Point()
            # point.x=x
            # point.y=y
            point.x = 6.0
            point.y = 0.0
            point.z=0.0

            self.counter+=1
            self.stampedpoint.header.seq=self.counter
            self.stampedpoint.header.frame_id="base_link"
            self.stampedpoint.header.stamp=time
            #rospy.loginfo("point: %s" % str(point))
            self.stampedpoint.point=point
            self.cd_pub.publish(self.stampedpoint)
            
            scan=LaserScan()
            scan.header=msg.header
            scan.angle_min=self.phi_start
            scan.angle_max=self.phi_end
            scan.angle_increment=msg.angle_increment
            scan.time_increment=msg.time_increment
            time=rospy.Time.now()
            scan.scan_time=time
            scan.range_min=msg.range_min
            scan.range_max=msg.range_max
            scan.ranges=msg.ranges[start_point:end_point]
            self.scan_window.publish(scan)

        else:
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


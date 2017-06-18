#!/usr/bin/env python  
import rospy

from std_msgs.msg import Int16
from project1_solution.msg import TwoInts

def callback(data):
  rospy.loginfo(rospy.get_caller_id() + "I heard {} and {}".format(data.a, data.b))
  #rospy.loginfo('data.a={} data.b={}'.format(data.a, data.b))
  s = data.a + data.b
  pub = rospy.Publisher('sum', Int16, queue_size=10)
  pub.publish(s)
  
def listener():
    
  rospy.init_node('listener', anonymous=True)
 
  rospy.Subscriber("two_ints", TwoInts, callback)
    
  rospy.spin()
 
if __name__ == '__main__':
  listener()




  
#!/usr/bin/env python  
import rospy

import math

import tf
import tf2_ros
import geometry_msgs.msg
import numpy as np

def publish_transforms():
    object_transform = geometry_msgs.msg.TransformStamped()
    object_transform.header.stamp = rospy.Time.now()
    object_transform.header.frame_id = "base_frame"
    object_transform.child_frame_id = "object_frame"    
    q1 = tf.transformations.quaternion_from_euler(0.79, 0.0, 0.79)
    object_transform.transform.rotation.x = q1[0]
    object_transform.transform.rotation.y = q1[1]
    object_transform.transform.rotation.z = q1[2]
    object_transform.transform.rotation.w = q1[3]
    T = tf.transformations.translation_matrix((0.0, 1.0, 1.0))
    R = tf.transformations.quaternion_matrix(q1)
    M_b_o = tf.transformations.concatenate_matrices(R, T)
    T = tf.transformations.translation_from_matrix(M_b_o)
    object_transform.transform.translation.x = T[0]
    object_transform.transform.translation.y = T[1]
    object_transform.transform.translation.z = T[2]       
    br.sendTransform(object_transform)
    
    
    robot_transform = geometry_msgs.msg.TransformStamped()
    robot_transform.header.stamp = rospy.Time.now()
    robot_transform.header.frame_id = "base_frame"
    robot_transform.child_frame_id = "robot_frame"
    q2 = tf.transformations.quaternion_about_axis(1.5, (0,0,1))
    robot_transform.transform.rotation.x = q2[0]
    robot_transform.transform.rotation.y = q2[1]
    robot_transform.transform.rotation.z = q2[2]
    robot_transform.transform.rotation.w = q2[3]
    T2 = tf.transformations.translation_matrix((0.0, -1.0, 0.0))
    R2 = tf.transformations.quaternion_matrix(q2)
    M_b_r = tf.transformations.concatenate_matrices(R2, T2) 
    
    T = tf.transformations.translation_from_matrix(M_b_r)
    robot_transform.transform.translation.x = T[0]
    robot_transform.transform.translation.y = T[1]
    robot_transform.transform.translation.z = T[2]  
    #robot_transform.transform.translation.x = 0.0
    #robot_transform.transform.translation.y = -1.0
    #robot_transform.transform.translation.z = 0.0
    br.sendTransform(robot_transform)    
    
    
    M_r_c = tf.transformations.translation_matrix((0.0, 0.1, 0.1))
    M_b_c = np.dot(M_b_r, M_r_c)
    M_c_o = np.dot(tf.transformations.inverse_matrix(M_b_c), M_b_o)
    v_c_o = tf.transformations.translation_from_matrix(M_c_o)
    v_c_o = tf.transformations.unit_vector(v_c_o)
    #print(v_c_o)    
    x_axis = (1, 0, 0)
    alpha = math.acos(np.dot(v_c_o, x_axis))
    #print(alpha)
    w = np.cross(v_c_o, x_axis)
     
    camera_transform = geometry_msgs.msg.TransformStamped()
    camera_transform.header.stamp = rospy.Time.now()
    camera_transform.header.frame_id = "robot_frame"
    camera_transform.child_frame_id = "camera_frame"
    q3 = tf.transformations.quaternion_about_axis(alpha, -w)
    camera_transform.transform.rotation.x = q3[0]
    camera_transform.transform.rotation.y = q3[1]
    camera_transform.transform.rotation.z = q3[2]
    camera_transform.transform.rotation.w = q3[3]   
    camera_transform.transform.translation.x = 0.0
    camera_transform.transform.translation.y = 0.1
    camera_transform.transform.translation.z = 0.1    
    br.sendTransform(camera_transform)

if __name__ == '__main__':
    rospy.init_node('project2_solution')

    br = tf2_ros.TransformBroadcaster()
    rospy.sleep(0.5)

    while not rospy.is_shutdown():
        publish_transforms()
        rospy.sleep(0.05)

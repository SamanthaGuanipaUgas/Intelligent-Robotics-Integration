#!/usr/bin/env python3
import rospy
import numpy as np
from rospy import Time
from std_msgs.msg import Float32
from sensor_msgs.msg import JointState

# Define the callback functions
def tau_callback(msg):
    global Tau
    Tau = msg.data

def slm_manipulator():
    global k, m, l, g, Tau, x1, x2, dt
    k = 0.01
    m = 0.75
    l = 0.36
    g = 9.8
    Tau = 0.0
    x1 = 0.0
    x2 = 0.0
    dt = 1/100  # frequency
    rate = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        a = l / 2
        J = (4 / 3) * m * a ** 2
        x1 += x2 * dt
        x2_dot = 1 / J * (Tau - m * g * a * np.cos(x1) - k * x2)
        x2 += x2_dot * dt

        # Setup of publishers
        pub = rospy.Publisher("/joint_states", JointState, queue_size=10)
        msg = JointState()
        msg.header.stamp = rospy.Time.now()
        msg.name = ["joint2"]
        msg.position = [wrap_to_Pi(x1)]
        msg.velocity = [x2]
        pub.publish(msg)
        rate.sleep()

# Wrap to pi function
def wrap_to_Pi(theta):
    result = np.fmod((theta + np.pi), (2 * np.pi))
    if result < 0:
        result += 2 * np.pi
    return result - np.pi

if __name__ == '__main__':
    # Initialize and Setup node
    rospy.init_node("SLM_Sim")
    rospy.loginfo("Node slm_sim has been started")

    # Configure the Node
    loop_rate = rospy.Rate(rospy.get_param("~node_rate", 100))

    # Setup the Subscribers
    rospy.Subscriber("/tau", Float32, callback=tau_callback)
    print("The SLM sim is Running")
    try:
        slm_manipulator()
        loop_rate.sleep()

    except rospy.ROSInterruptException:
        pass

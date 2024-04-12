#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32

if __name__=='__main__':
    #Iniciar el nodo
    rospy.init_node("nodotau")
    #Enviar mensaje de inicio del nodo
    rospy.loginfo("Nodo tau inicializado")
    #Crear publisher, usando el nombre del topico y el mensaje
    pub = rospy.Publisher("/tau",Float32, queue_size=10)
    rate = rospy.Rate(2)
    while not rospy.is_shutdown():
        #se establece tau
        tau = 0.0
        #Publicar tau
        pub.publish(tau)
        rate.sleep()
        

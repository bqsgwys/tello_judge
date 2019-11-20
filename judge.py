#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import rospy
import threading
from std_msgs.msg import String,Int16,Bool

global score, time_start, time_end
global already_takeoff, already_seenfire, already_seentarget
global targets, is_fail
global fail_pub
score = 0
if_fail = False
already_takeoff = False
already_seenfire = False
already_seentarget = [False, False, False]
score_lock = threading.Lock()
time_start_lock = threading.Lock()
time_end_lock = threading.Lock()

def scoreTakeoff(data, groupid):
    global score,time_start,already_takeoff,is_fail
    ready = data.data
    if is_fail:
        return
    if ready:
        rcvd_pub = rospy.Publisher(groupid+'/received', Int16, queue_size=3)
        rcvd_pub.publish(1)

        score_lock.acquire()
        if not already_takeoff:
            score += 20
            already_takeoff = True
        score_lock.release()

        time_start_lock.acquire()
        time_start = time.time()
        time_start_lock.release()

    print('takeoff: ',score,time_start)


def scoreFire(data, groupid):
    global score,already_seenfire,is_fail
    if is_fail:
        return

    seen_fire = data.data
    if seen_fire:
        score_lock.acquire()
        if not already_seenfire:
            score += 20
            already_seenfire = True
        score_lock.release()

    print('fire: ',score)


def scoreTgt1(data, groupid):
    global score,targets,already_seenfire,already_seentarget,is_fail,fail_pub
    if is_fail:
        return

    target = data.data
    if already_seenfire and (target==targets[0]):
        score_lock.acquire()
        if not already_seentarget[0]:
            score += 20
            already_seentarget[0] = True
        score_lock.release()
        tgt1_pub = rospy.Publisher(groupid+'/receviedtarget1', Int16, queue_size=3)
        tgt1_pub.publish(1)
    else:
        fail_pub.publish(1)
        is_fail = True

    print('target1: ',score,already_seentarget)


def scoreTgt2(data, groupid):
    global score,targets,already_seentarget,is_fail,fail_pub
    if is_fail:
        return

    target = data.data
    if already_seentarget[0] and (target==targets[1]):
        score_lock.acquire()
        if not already_seentarget[1]:
            score += 20
            already_seentarget[1] = True
        score_lock.release()
        tgt2_pub = rospy.Publisher(groupid+'/receviedtarget2', Int16, queue_size=3)
        tgt2_pub.publish(1)
    else:
        fail_pub.publish(1)
        is_fail = True

    print('target2: ',score,already_seentarget)
    

def scoreTgt3(data, groupid):
    global score,targets,already_seentarget,is_fail,fail_pub
    if is_fail:
        return

    target = data.data
    if already_seentarget[0] and already_seentarget[1] and (target==targets[2]):
        score_lock.acquire()
        if not already_seentarget[2]:
            score += 20
            already_seentarget[2] = True
        score_lock.release()
        tgt3_pub = rospy.Publisher(groupid+'/receviedtarget3', Int16, queue_size=3)
        tgt3_pub.publish(1)
    else:
        fail_pub.publish(1)
        is_fail = True
        
    print('target3: ',score,already_seentarget)


def done(data, groupid):
    global score,time_start,time_end,is_fail
    complete = data.data
    if is_fail:
        return
    if complete:
        time_end_lock.acquire()
        time_end = time.time()
        time_end_lock.release()
        
    print('done: ',score,time_end-time_start)


def sub_thread(topic, callback):
    rospy.Subscriber(topic, Int16, callback, groupid)


if __name__ == '__main__':
    # initiate
    groupid = '/group'+str(1)    # your group id
    targets = [1,2,3]            # your targets id

    score = 0
    is_fail = False
    already_takeoff = False
    already_seenfire = False
    already_seentarget = [False, False, False]

    rospy.init_node('judge', anonymous=True)

    fail_pub = rospy.Publisher(groupid+'/failure', Int16, queue_size=3)

    takeoff_sub_thread = threading.Thread(target = sub_thread, args=(groupid+"/takeoff", scoreTakeoff))
    takeoff_sub_thread.start()
    fire_sub_thread = threading.Thread(target = sub_thread, args=(groupid+"/seenfire", scoreFire))
    fire_sub_thread.start()
    tgt1_sub_thread = threading.Thread(target = sub_thread, args=(groupid+"/seentarget1", scoreTgt1))
    tgt1_sub_thread.start()
    tgt2_sub_thread = threading.Thread(target = sub_thread, args=(groupid+"/seentarget2", scoreTgt2))
    tgt2_sub_thread.start()
    tgt3_sub_thread = threading.Thread(target = sub_thread, args=(groupid+"/seentarget3", scoreTgt3))
    tgt3_sub_thread.start()
    done_sub_thread = threading.Thread(target = sub_thread, args=(groupid+"/done", done))
    done_sub_thread.start()
    
    input()


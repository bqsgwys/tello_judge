# tello_judge

这是比赛选手本地可以运行的裁判模拟器，主要有以下功能：

- 读取/groupid/takeoff 话题的消息 ，话题的内容是0或者1，1表示无人机准备完毕，请求起飞。 
- 读到请求信号后，如果当前是当前正在比赛的组别，向/groupid/received 话题发送起飞准许，话题内容是1，假如不是，发送0。score+=20，开始计时
- 读取/groupid/seenfire 话题，内容是0或者1 ，1表示无人机已经成功穿过着火点。 score+=20
- 读取/groupid/seentarget1 话题，内容是物体的id，也就是数字1-5，判断与系统存储的数字是否一致，如果一致，score+=20，并向/groupid/receviedtarget1 话题发送1，表示已经收到，可以向下进行。
- 同上，还有/groupid/seentarget2和/groupid/seentarget3，注意必须先匹配1然后再匹配2和3，识别是有顺序的。
- 如果接收到的结果和系统存储的数字不一致，向 /groupid/failure 发送1，表示任务失败。 
- 读取/groupid/done 话题，收到1表示无人机完成任务，已经降落，score+=20，结束计时。

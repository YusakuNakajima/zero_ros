import rtde_control
import rtde_receive
import time
robot_ip = "URロボットのIPアドレス" 
rtde_c = rtde_control.RTDEControlInterface(robot_ip)
rtde_r = rtde_receive.RTDEReceiveInterface(robot_ip)
try:
    # PTP動作 (関節空間)
    # 関節角度をラジアンで指定
    target_joints = [0.1, -1.2, 2.3, -1.5, 0.5, 0.0] #ラジアン表記
    rtde_c.moveJ(target_joints, 1.0, 0.5) # 速度1.0rad/s, 加速度0.5rad/s^2
    time.sleep(5)

    # LIN動作 (ベース座標系)
    # ベース座標系での目標TCP位置を指定,  [x, y, z, rx, ry, rz] (単位: [m, rad])
    target_pose_base = [0.3, 0.4, 0.5, 0.0, 0.0, 0.0]
    rtde_c.moveL(target_pose_base, 0.5, 0.3) # 速度0.5m/s, 加速度0.3m/s^2
    time.sleep(5)

    # CIRC動作 (ツール座標系)
    # ツール座標系での中間点と目標点のTCP位置を指定,  [x, y, z, rx, ry, rz] (単位: [m, rad])
    via_pose_tool = [0.1, 0.1, 0.0, 0.0, 0.0, 0.0]
    to_pose_tool = [0.2, 0.0, 0.0, 0.0, 0.0, 0.0]
    rtde_c.moveC(via_pose_tool, to_pose_tool, 0.5, 0.3, pose_tool=True) # 速度0.5m/s, 加速度0.3m/s^2
    time.sleep(5)

finally:
    rtde_r.disconnect()

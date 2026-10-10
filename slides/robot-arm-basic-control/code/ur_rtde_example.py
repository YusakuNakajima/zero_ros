import rtde_control
rtde_c = rtde_control.RTDEControlInterface("URロボットのIPアドレス")

# PTP ⇔ movej(q, a=1.4, v=1.05)  ※ ur_rtde は (位置, speed, acceleration) の順
rtde_c.moveJ([0, -1.57, 1.57, 0, 1.57, 0], 1.05, 1.4)

# LIN ⇔ movel(p[...], a=1.2, v=0.25)
rtde_c.moveL([0.3, -0.2, 0.25, 0, 3.14, 0], 0.25, 1.2)

# ブレンド ⇔ r=0.05：経路で渡す（各点 = pose + [speed, acceleration, blend]）
rtde_c.moveL([[0.35, -0.1, 0.25, 0, 3.14, 0, 0.25, 1.2, 0.05],
              [0.3, 0.0, 0.25, 0, 3.14, 0, 0.25, 1.2, 0.0]])  # 最後は blend=0

rtde_c.stopScript()

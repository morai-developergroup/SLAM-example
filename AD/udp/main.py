import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from network.udp_manager import UdpManager
from autonomous_driving.autonomous_driving import AutonomousDriving


def main():
    autonomous_driving = AutonomousDriving()
    udp_manager = UdpManager(autonomous_driving)
    udp_manager.execute()


if __name__ == '__main__':
    main()

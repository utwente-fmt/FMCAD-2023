import sys

from examples.robot.robot import Robot as Robot
from examples.robot_dummy.robot import Robot as RobotDummy
from examples.robot_1MS.robot import Robot as Robot1MS
from examples.prod_cons.prod_cons import ProdCons
from examples.absasr.absasr import AbsAsr

if __name__ == "__main__":
    
    p = Robot()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "robot":
            pass
        elif sys.argv[1] == "robot-dummy":
            p = RobotDummy()
        elif sys.argv[1] == "robot-1MS":
            p = Robot1MS()
        elif sys.argv[1] == "prod-cons":
            p = ProdCons()
        elif sys.argv[1] == "abs-asr":
            p = AbsAsr()
        else:
            print("Wrong option <{}>.".format(sys.argv[1]))
            print("Options are: robot, robot-dummy, robot-1MS, prod-cons, abs-asr")
            exit(0)
            
    p.simulate()


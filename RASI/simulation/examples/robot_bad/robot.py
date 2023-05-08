from simulator.main import Main
from .sensor import Sensor
from .controller import Controller
from .bad import Bad

MIN   = 45

class Robot (Main) :

    def simulate(self):

        m = Main()
        
        # register events
        
        SENSORWAIT = 0
        CONTROLLERWAIT = 1
        BADWAIT = 2
        OBSTACLEDETECTED = 3

        m.register_event(SENSORWAIT, "sensor_wait")
        m.register_event(CONTROLLERWAIT, "controller_wait")
        m.register_event(BADWAIT, "bad_wait")
        m.register_event(OBSTACLEDETECTED, "obstacle_detected")
        
        # add extra variables
        
        # build non processes
        
        # register process
        
        sensor = Sensor(SENSORWAIT, OBSTACLEDETECTED, MIN, -1, "sensor",
            m.wait,m.notify,m.set_pc,m.change_state,m.save_state,m.check_state)
        pid = m.register_process(sensor)
        sensor.set_pid(pid)
        
        controller = Controller(CONTROLLERWAIT, OBSTACLEDETECTED, -1, "controller",
            m.wait,m.notify,m.set_pc,m.change_state,m.save_state,m.check_state)
        pid = m.register_process(controller)
        controller.set_pid(pid)
        
        bad = Bad(BADWAIT, sensor, -1, "bad", 
            m.wait,m.notify,m.set_pc,m.change_state,m.save_state,m.check_state)
        pid = m.register_process(bad)
        bad.set_pid(pid)

        m.simulate()

if __name__ == "__main__":
    r = Robot()
    r.run()

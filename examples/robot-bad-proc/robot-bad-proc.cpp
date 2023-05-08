#include <systemc.h>
#include <stdio.h>
#include <stdlib.h>


#define MIN_DIST 50

SC_MODULE(Robot) {

public:
    sc_event obs_detected;
    int dist;

    SC_CTOR(Robot) {
        dist = 256;
        SC_THREAD(sensor);
        SC_THREAD(controller);
        SC_THREAD(bad)
    }

    int read_sensor(int x) {
        return rand() % 256;
    }

    void sensor() {
        
        while(true) {
            wait(2, SC_MS);
            // read from sensor values between 0 and 255
            dist = read_sensor(dist);
            // collision possibility detection
            if(dist < MIN_DIST) {
                cout << "Obstacle detected.\n";
                obs_detected.notify(SC_ZERO_TIME);
            }else{
                cout << "No obstacle around.\n";
            }
        }
    }
	
    void controller() {
        bool alarm_flag = false;
        while (true) {
            // waiting for event
            wait(obs_detected);
            cout << "Setting the flag.\n";
            alarm_flag = true;
        }
    }
    
    void bad() {
        while (true) {
            wait(1, SC_MS);
            dist = rand()%256;
            cout << "Bad proc changed dist to " << dist << ".\n";
        }
    }
};


int sc_main (int argc, char* argv[]) {
    Robot robot("Robot0");
    sc_start(200 ,SC_MS);
    return(0);
}

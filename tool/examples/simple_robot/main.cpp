#include <systemc.h>
#include "Robot.h"

int sc_main (int argc, char* argv[]) {
    srand(time(NULL));
    Robot robot("Robot0");
    sc_start(20 ,SC_MS);
    return(0);
}

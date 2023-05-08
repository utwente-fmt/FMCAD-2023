#include <systemc.h>
#include <cstdlib>
#include <ctime>
#include "settings.h"

#ifndef TICK_COUNTER_H
#define TICK_COUNTER_H

SC_MODULE ( TickCounter ) {

//-*-*-*-*-*-*-*-*-*-*-*-*  INTERFACE  *-*-*-*-*-*-*-*-*-*-*-*-

  sc_fifo_out<int> out; 

//-*-*-*-*-*-*-*-*-*-*-*-* LOCAL VARIABLES *-*-*-*-*-*-*-*-*-*-*-*-
  int ticks;       // Counter

//-*-*-*-*-*-*-*-*-*-*-*-*-* COUNTER *-*-*-*-*-*-*-*-*-*-*-*-*-
  
  /* void count(){
    if (reset.read())
      ticks = 0;
    else
      ticks = ticks + 1;
      }*/
 
//-*-*-*-*-*-*-*-*-*-*-*-*-* SENDER *-*-*-*-*-*-*-*-*-*-*-*-*-
  
  // read ticks in a given time interval and send to ECU
  void send(){
    int speed;

    srand(time(NULL));
    while(true){
      wait(TICKPERIOD, SC_MS);
/* #ifdef DEBUG */
/* 	cout << sc_time_stamp() << " trying to send to ECU: " << ticks << endl; */
/* #endif */
      speed = rand();
      out.write(speed); // zur ECU schicken  
/* #ifdef DEBUG */
/* 	cout << sc_time_stamp() << " send to the ECU: " << ticks << endl; */
/* #endif */
//	ticks = 0; 
    }
  }

//-*-*-*-*-*-*-*-*-*-*-*-*-*-* CONSTRUCTOR *-*-*-*-*-*-*-*-*-*-*-*-*-*-
  
  SC_CTOR(TickCounter) {
    //    SC_METHOD(count);
    //sensitive << inTicks;
    SC_THREAD(send);
    
  } 

}; 

#endif

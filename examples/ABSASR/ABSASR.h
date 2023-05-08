/* This is a simple Anti-lock Braking System. The inputs are the
   number of ticks counted within 100 ms at each wheel. Outputs are
   control signals for pressure control (0 - constant pressure, 2 -
   increase pressure, 1 - increase pressure slightly, -1 - decrease
   pressure).

   would be better: move conversion from ticks to velocity to other
   modules, would be easier then to argue with a real refinement
   process (communication, data and time refinement)
*/

#include <systemc.h>
#include "settings.h"

#ifndef ABSASR_H
#define ABSASR_H

SC_MODULE ( ABSASR ) {

//-*-*-*-*-*-*-*-*-*-*-*-*  INTERFACE  *-*-*-*-*-*-*-*-*-*-*-*-

  sc_fifo_in<int>  bus_vl;
  sc_fifo_in<int>  bus_vr;
  sc_fifo_in<int>  bus_hl;
  sc_fifo_in<int>  bus_hr;

//-*-*-*-*-*-*-*-*-*-*-*-* LOCAL VARIABLES *-*-*-*-*-*-*-*-*-*-*-*-

//  int ticks_vr, ticks_vl, ticks_hr, ticks_hl;
  int v[4], a[4]; // current wheel velocity and acceleration
  int temp_fv, fv; // estimated vehicle velocity
  int fa; // estimated vehicle acceleration
  int lambda[4]; // Slippage at each wheel
  int s[4]; // ABS state per wheel
  int p[4]; // Braking pressure command (see above)

  // ABS Routine
  void _ABS(){

    if(fv > ABSACTIVE){    // ABS is only active above a threshold velocity

      #ifdef DEBUG
        cout << sc_time_stamp() << " ABS greift ein " << endl;
      #endif

      for(int i = 0; i < 4; i = i + 1){
        lambda[i] = ((fv-v[i])*100)/fv;

        #ifdef DEBUG
          cout << sc_time_stamp() << " lambda[" << i << "]: " << lambda[i] << endl;
          cout << sc_time_stamp() << " v[" << i << "]: " << v[i] << endl;
          cout << sc_time_stamp() << " a[" << i << "]: " << a[i] << endl;
        #endif

        switch(s[i]){
          case 1:
            if (a[i] < minus_a){
              p[i] = 0;
              s[i] = 2;
            }
            break;
          case 2:
            if (lambda[i] > lambda_abs){
              p[i] = -1;
              s[i] = 3;
            }
            break;
          case 3:
            if (a[i] > minus_a){
              p[i] = 0;
              s[i] = 4;
            }
            break;
          case 4:
            if (a[i] > plus_A){
              p[i] = 2;
              s[i] = 5;
            }
            break;
          case 5:
            if (a[i] < plus_A){
              p[i] = 0;
              s[i] = 6;
            }
            break;
          case 6:
            if (a[i] < plus_a){
              p[i] = 1;
              s[i] = 7;
            }
            break;
          case 7:
            if (a[i] < minus_a){
              p[i] = -1;
              s[i] = 8;
            }
            break;
          case 8:
            if (a[i] > minus_a){
              p[i] = 0;
              s[i] = 4;
            }
            break;
        }
      }
    }
  }

  // ASR Routine
  void _ASR(){

    int j = 3; // the first comparison is vl (0) with hr (3)
               // ASR assumes front wheel drive

    for(int i = 0; i < 2; i = i + 1){

      if(v[i] > 0){
        lambda[i] = ((v[i]-v[j])*100)/v[i];

        if(lambda[i] > lambda_asr){ // Slippage too high -> brake
          if(a[i] > 0){
            p[i] = 2;   // Increase pressure
          }
          else{
            p[i] = 0;  // Keep pressure constant
          }
        }
        else{ // No slippage -> release brakes
          p[i] = -1;  // Release braking pressure
        }
      }
      j = 2; // the second comparison is vr (1) with hl (2)
    }
  }

  int abs(int val)
    {
      if (val >= 0)
        return val;
      else
        return -val;
    }

  void not_a_main()
    {
      int i;
      // INIT
      for(i = 0; i < 4; i=i+1){
        s[i] = 1;
        v[i] = 0;
        a[i] = 0;
      }

      while(true){
        wait(1,SC_MS);

        // Take the velocity of the wheel with the lowest acceleration as a reference for the vehicle velocity
        i = 0;
        if(abs(a[1]) < abs(a[i]))
          i = 1;
        if(abs(a[2]) < abs(a[i]))
          i = 2;
        if(abs(a[3]) < abs(a[i]))
          i = 3;

        temp_fv = v[i];
        fa = temp_fv - fv;

        #ifdef DEBUG
          cout << endl;
          cout << sc_time_stamp() << " aktuelle Geschwindigkeit: " << temp_fv << endl;
          cout << sc_time_stamp() << " v[0]: " << v[0] <<  ", v[1]: " << v[1] << ", v[2]: " << v[2] << ", v[3]: " << v[3] << endl;
          cout << sc_time_stamp() << " aktuelle Beschleunigung: " << fa << endl;
          cout << sc_time_stamp() << " a[0]: " << a[0] <<  ", a[1]: " << a[1] << ", a[2]: " << a[2] << ", a[3]: " << a[3] << endl;
        #endif

        if( fa < 0 ){ //  deceleration
          if(fa < minus_a){  // all wheels are locked -> use different estimation for vehicle velocity
            fv=fv+AREF; // estimated optimal deceleration

            #ifdef DEBUG
              cout << sc_time_stamp() << " alle Raeder haben Blockierneigung! " << endl;
              cout << sc_time_stamp() << " geschaetzte Geschwindigkeit: " << fv << endl;
            #endif
          }
          else
            fv = temp_fv;
          _ABS();
        }
        else if (fa > 0){
          fv = temp_fv;
          _ASR();
        }
      }
    }

  void read_speed()
    {
      int tmp_0 = 0;
      int tmp_1 = 0;
      int tmp_2 = 0;
      int tmp_3 = 0;
      while(true){
        v[0] = bus_vr.read();

        #ifdef DEBUG
          cout << sc_time_stamp() << " speed at right front wheel: "<< v[0] << endl;
        #endif

        //  v[0] = VELOFACTOR * ticks_vr;
        a[0] = (v[0] - tmp_0); //*VELOFACTOR;
        tmp_0 = v[0];

        // ----------------------------------

        v[1] = bus_vl.read();

        #ifdef DEBUG
          cout << sc_time_stamp() << " speed at left front wheel: "<< v[1] << endl;
        #endif

        //	  v[1] = VELOFACTOR * v[1];
        a[1] = (v[1] - tmp_1); //*VELOFACTOR;
        tmp_1 = v[1];

        // ----------------------------------

        v[2] = bus_hr.read();

        #ifdef DEBUG
          cout << sc_time_stamp() << " speed at right rear wheel: "<< v[2] << endl;
        #endif

        //	  v[2] = VELOFACTOR * v[2];
        a[2] = (v[2] - tmp_2); //*VELOFACTOR;
        tmp_2 = v[2];

        // ----------------------------------

        v[3] = bus_hl.read();

        #ifdef DEBUG
          cout << sc_time_stamp() << " speed at left rear wheel: "<< v[3] << endl;
        #endif

        //	  v[3] = VELOFACTOR * v[3];
        a[3] = (v[3] - tmp_3); //*VELOFACTOR;
        tmp_3 = v[3];
      }
    }

//-*-*-*-*-*-*-*-*-*-*-*-*-*-* KONSTRUKTOR *-*-*-*-*-*-*-*-*-*-*-*-*-*-

  SC_CTOR( ABSASR ){
    SC_THREAD(not_a_main);
    // read in the ticks and calculate a and v
    SC_THREAD(read_speed);
  }
};

#endif

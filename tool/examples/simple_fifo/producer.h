#ifndef PRODUCER_H
#define PRODUCER_H

#include <systemc.h>
#include <iostream>

SC_MODULE(producer)
{

    sc_port<myfifo_if> fifo;

    int pid;

    int produce(int c_param)
    {
      int wait_time = 100;
      wait(wait_time, SC_NS);
      c_param = (c_param + 1)%8;
      return c_param;
    }

    void main_method(void)
    {
      int c = 0;
      while(true)
      {
        fifo->write(c);
        c = produce(c);
      }
    }

    //    SC_HAS_PROCESS(producer);

    SC_CTOR(producer)
    {
	    SC_THREAD(main_method);
    }


};

#endif

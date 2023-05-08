#ifndef CONSUMER_H
#define CONSUMER_H

#include <systemc.h>
#include <iostream>

SC_MODULE(consumer)
{
    sc_port<myfifo_if> fifo;

    void consume(int c_param)
    {
      wait(200, SC_US);
      cout << sc_time_stamp() << " consumer: " << c_param << " consumed" << std::endl;
    }

    void main_method(void)
    {
      int c = 0;
      while(true)
      {
        c = fifo->read();
	    consume(c);
      }
    }


    SC_CTOR(consumer)
    {
    	SC_THREAD(main_method);
    }


};

#endif

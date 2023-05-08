#ifndef MYFIFO_H
#define MYFIFO_H
#define BUFFERSIZE 4
class myfifo_if : 
virtual public sc_interface 
{
  public:
    virtual void write(int c) = 0;
    virtual int read(void) = 0;
};

class myfifo : 
public sc_channel, public myfifo_if 
{

  private:

    int buffer[BUFFERSIZE];
    int n, r_pos, w_pos;
  public: 
    sc_event w_event, r_event;
 
    SC_CTOR(myfifo){
      n = 0;
      r_pos = 0;
      w_pos = 0;
    }  

  void write(int c) 
  {
    if (n == BUFFERSIZE)
	{
	wait(r_event);
      }
    if (c == 8)
      cout << "fifo: input " << c << endl;
    buffer[w_pos] = c;
    n = n + 1;
    w_pos = (w_pos + 1)%BUFFERSIZE;
    w_event.notify(0, SC_NS);
  }

  int read(void) 
  {
    int c;
    if (n == 0)
      {
	wait(w_event);
      }
    c = buffer[r_pos];
    n = n - 1;
    r_pos = (r_pos + 1)%BUFFERSIZE;
    r_event.notify(0, SC_NS);
    return c;
  }
};
#endif

#include <systemc.h>
#include "myfifo.h"
#include "producer.h"
#include "consumer.h"

int sc_main(int argc, char* argv[])
{
    myfifo fifo_inst("thisfifo");
    producer prod_inst("producer");
    consumer cons_inst("consumer");
    prod_inst.fifo(fifo_inst);
    cons_inst.fifo(fifo_inst);
    sc_start(5000,SC_NS);
    return 0;
}

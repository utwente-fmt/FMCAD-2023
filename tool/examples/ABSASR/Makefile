UNIT = ABS_tb

OBJS = $(UNIT).o 
TARGET = $(UNIT)

# installation path
#SYSTEMC = $(HOME)/systemc/systemc-2.1.v1
CXX = g++
CC = gcc

LIBDIR = -L $(SYSTEMC_HOME)/lib-linux64
INCDIR = -I $(SYSTEMC_HOME)/include
LIBS =  -lsystemc -lm $(EXTRA_LIBS)

all: $(TARGET)

$(TARGET): $(OBJS)
	 $(CXX) $(CFLAGS) $(INCDIR) $(LIBDIR) -o $@ $(OBJS) $(LIBS)

#%.o: %.cpp
#	 $(CXX) $(CFLAGS) $(INCDIR) -g -c -Wno-deprecated $< -o $@

$(UNIT).o: $(UNIT).cpp 
	 $(CXX) $(CFLAGS) $(INCDIR) -g -c -Wno-deprecated $< -o $@
	 
ast:
	java -jar $(SC2AST) -f  $(UNIT).cpp -o $(UNIT)_ast

uppaal:
	java -jar $(SC2AST) -f settings.h TickCounter.h ABSASR.h inputgen.h outputmon.h ABS_tb.cpp -o $(UNIT)_ast
	../../state.sh $(UNIT)_ast.ast.xml $(UNIT).uppaal.xml  $(UNIT).tb



clean:
	rm -f $(OBJS) $(TARGET) *~

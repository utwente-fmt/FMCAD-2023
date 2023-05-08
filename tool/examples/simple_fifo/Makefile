UNIT = prod_cons

OBJS = $(UNIT).o
TARGET = $(UNIT)

# installation path
#SYSTEMC = $(HOME)/systemc/systemc-2.1.v1
CXX = g++
CC = gcc
CFLAGS = -fpermissive

ARCH ?= $(shell uname -m)
ifeq ($(ARCH),x86_64)
LIBDIR = -L $(SYSTEMC_HOME)/lib-linux64
else
LIBDIR = -L $(SYSTEMC_HOME)/lib-linux
endif

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
	java -jar $(SC2AST) -f  prod_cons.cpp -o $(UNIT)_ast

uppaal:
	java -jar $(SC2AST) -f  prod_cons.cpp -o $(UNIT)_ast
	$(STATE_HOME)/state.sh $(UNIT)_ast.ast.xml $(UNIT).uppaal.xml  $(UNIT).tb

clean:
	rm -f $(OBJS) $(UNIT)_ast $(UNIT)_ast.ast.xml $(TARGET) *~

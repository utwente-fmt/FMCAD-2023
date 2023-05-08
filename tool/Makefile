JAVA = java # set the path to your java>16 installation

ast:
	$(JAVA) -jar sc2ast.jar -f  ./examples/simple_fifo/prod_cons.cpp -o ./examples/simple_fifo/main_ast
	$(JAVA) -jar sc2ast.jar -f  ./examples/simple_robot/main.cpp -o ./examples/simple_robot/main_ast
	$(JAVA) -jar sc2ast.jar -f  ./examples/ABSASR/ABS_tb.cpp -o ./examples/ABSASR/main_ast

fifo: 	ast
	if ! test -d ./results/simple_fifo/; \
	then mkdir -p ./results/simple_fifo/; \
	fi
	$(JAVA) -jar sc2pvl.jar -i ./examples/simple_fifo/main_ast.ast.xml -o ./results/simple_fifo/ -tr 1

robot: 	ast
	if ! test -d ./results/simple_robot/; \
	then mkdir -p ./results/simple_robot/; \
	fi
	$(JAVA) -jar sc2pvl.jar -i ./examples/simple_robot/main_ast.ast.xml -o ./results/simple_robot/ -tr 1000000
	
absasr: ast
	if ! test -d ./results/ABSASR/; \
	then mkdir -p ./results/ABSASR/; \
	fi
	$(JAVA) -jar sc2pvl.jar -i ./examples/ABSASR/main_ast.ast.xml -o ./results/ABSASR/ -tr 1

all: fifo robot absasr

clean:
	rm -rf ./results
	rm -f ./examples/simple_fifo/*.xml
	rm -f ./examples/simple_fifo/main_ast
	rm -f ./examples/simple_robot/*.xml
	rm -f ./examples/simple_robot/main_ast
	rm -f ./examples/ABSASR/*.xml
	rm -f ./examples/ABSASR/main_ast

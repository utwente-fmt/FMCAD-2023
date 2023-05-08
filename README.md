# FMCAD 2023

Case studies and tools to support the submission of our paper "Deductive Verification of Parameterized Embedded Systems modeled in SystemC" to FMCAD 2023.

## Case studies

In the **examples** folder you can find the various versions of the robot case study and the producer consumer case study mentioned in the Evaluation section (Sec. 5) of our paper. Each subfolder contains both the original SystemC design (which you can compile and simulate with SystemC) and a pvl file with our transformation. The pvl files also contain the RASI invariant and are anotated with program counters. The robot and robot-1MS examples are also anotated with a property to verify. You can verify any of this files with VerCors by calling
> `vct --silicon <file_name>.pvl`

For your convenience, we list here the experimental results also found in Sec. 5 of our paper

| Design | # processes | # manual invariants | RASI size | Verification time | Result |
|--------|-------------|---------------------|-----------|-------------------|--------|
|robot|2|2|8|13s|&check;|
|robot-1MS|2|4|12|15s|&check;|
|robot-bad-timing|2|4|26|25s|&cross;|
|robot-dummy|3|4|24|34s|&check;|
|robot-bad-proc|3|4|24|33s|&cross;|
|producer-consumer|2|8|72|52s|&check;|
|ABS/ASR|6|9|247|10610s|&check;|


## Automatic transformation

The **tool** folder contains our tool for automatically generating the transformation from a SystemC design into pvl, following our paper. Instructions on how to run the tool and a short list of dependecies can be found in the README inside the **tool** folder.

## Reachable Abstract States Invariant (RASI) generation

The **RASI** folder contains scripts for generating the RASI for each of the case studies of the example folder. You can generate it as an over-approximation with the scripts in the *RASI/exploration* folder or as an under-approximation with the scripts in the *RASI/simulation* folder.

### Using the simulation tool
For the simulation tool, you need Python3. To generate the RASI for one of the _robot_ case studies, you can call
> ```python3 simulate.py name```

where ```name``` is one of `robot`, `robot-dummy`, `robot-bad`, `robot-1MS`, `robot-6MS`, `cons-prod`, `abs-asr`. The RASI will be printed to the standard output, along with the count of abstract states found. The result is an underapproximation of the reachable abstract state space. If any state is missing, VerCors will report that the invariants does not hold. You can then try to run the script again, and allow the randomness to find more states. You can also try to increase the amount of simulation runs `SIM_COUNT` or simulation length `SIM_LENGTH` in the `simulator/main.py` file.

### Using the exhaustive exploration tool
To use the exploration tool, navigate to the `exploration` folder, adjust the `main.py` and `simulator.py` files and then execute `main.py`. You need at least Python 3.7 to run the program. This will generate a full RASI including program counters and the length of the invariant.

To switch between different models, adjust the `n_proc`, `n_event` and `processes` attributes in `simulator`. `n_proc` should contain the number of processes (excluding the scheduler) and `n_event` should contain the number of events. The numbers can be found in the following table:

| Design | `n_event` | `n_proc` |
|--------|-----------|----------|
|robot-1MS|3|2|
|producer-consumer|4|2|
|ABS/ASR|17|6|

`processes` should contain a list of processes in order of their process ids, as well as the scheduler as the last entry in the list (the default is the ABS/ASR model; the process lists for the robot-1MS model and the producer-consumer model are commented out and can be uncommented to replace the ABS/ASR model). Additionally, you can change the process names in `main.py`.

To add data dependencies to the exploration, add the desired data variables (only integer variables are allowed) to the `sys_vars` list. You can read and modify these variables in the processes via the simulator's `modify_variable` and `get_variable_valuation` methods and use them as conditions for possible process transitions.

## Download VerCors

To reproduce the results from the paper, you should use the VerCors Snapshot 1.4.0 (https://github.com/utwente-fmt/vercors/releases/tag/v1.4.0). Binaries are available for Linux, Mac, and Windows. To verify a set of _pvl_ files, just run from the comand line
>```vct --silicon file1.pvl file2.pvl ... fileN.pvl```.

# RASI generation via simulation

Models to generate the RASI for the robot variants, the producer consumer design, and the abs/asr design can be found in the examples folder. Also, for each example, you can find in the corresponding folder the pvl code that follows the SystemC to PVL transformation described in the paper. These pvl files have been extended with the RASI, program counters, and properties to verify. To re-generate the RASI you can call the following command from your terminal

> `python3 simulate.py <example>`
    
where `<example>` is one of `robot`, `robot-1MS`, `robot-dummy`, `prod-cons`, `abs-asr`.
    
The RASI will be printed to your terminal's standard output stream. You can then copy it to the corresponding pvl file and run the verification on VerCors with the following command:

> `vct --silicon file1.pvl file2.pvl ... fileN.pvl`

For the ABSASR example, the invariants are located in the `main.pvl` file.
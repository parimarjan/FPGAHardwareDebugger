Hardware Debugger for FPGA's

Team Members: Rishab Mehra, Parimarjan Negi

Project Description:

Currently all the available debuggers are software based, where you can create the circuit/modules and see their outputs over different inputs. Our goal is to transfer this process to the hardware itself, and debug it right on the hardware. This skips the step of having to create the circuit in the simulator and helps debug the actual circuit itself rather than a virtually simulated version of it.

By the time we are done, we hope to have implemented a UART debugger, which is able to send an input array to a hardware module on an FPGA (via a shift register), and it receives back an output array. This will help us test and debug individual modules on the hardware itself.

While writing code for this class, we found the debugging process rather challenging, since there was no good way to debug our code unless we downloaded additional software and exported our code to Verrilator or a software alike. After discussing with Ross, we realized that the idea of a hardware debugger will be fun to make, and extremely useful. We skip the middle step of using a software debugger and at the same time are able to test the modules where they will actually be running - the hardware.

As mentioned before there are multiple software debuggers available, which we will use as a guideline, but no previous work has been done in making a debugger on the hardware itself.

Plan/Timeline:

The first major task is to get the UART protocol running and send an input array to the FPGA using a shift register on Magma. From there we will connect the input array to the circuit, making sure that everything in the circuit is hooked up to an enable, which turns on once when the input array changes, and we get back a new output array, which we can read using UART.

To implement the UART protocol we will first implement the printf shown in class and proceed to expand it from there and implement the shift register. For hooking up the circuits, we are considering changing the Magma primitives to have an addition parameter called debug (which can possibly be a global variable, or a parameter to the modules) and then setting the enable accordingly. 

Although, we both will be working together on all the tasks, Rishab will first start with trying to set up, and Negi will work on changing the Magma primitives. From there we will merge our work together and work towards getting the debugger ready.

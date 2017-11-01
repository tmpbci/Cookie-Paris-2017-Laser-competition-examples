Empty Laser 
By Sam Neurohack
LICENCE : CC

Needs : an etherdream DAC, an ILDA laser, RJ 45 IP network
 
You get a basic pygame skeleton with an onscreen simulator that can handle the laser drawing with an onscreen simulator.
This Empty Laser is mainly a Laser Hexagon (see /tmp/lab github) structure with some extras, like alignement keys. Many things are still in the todo list as how to store the align parameters for the next run.

In this version to bootstrap demomakers there is a basic different demostates paradigm.



Install :

Pygame 1.9 and its dependancies.
on OS X :

sudo easy_install pygame


To run : 

python main.py


you can change the demo state value to see different examples.


For more advanced code with text, sounds, gamepads,... you may look at these repositories :

https://github.com/tmplab
https://github.com/echelon
https://github.com/BlackBoxe



This program assumes that the ether dream is auto configured in a certain way especially for its IP address. Write an autoplay.txt file inside an SD Card within the ether dream DAC, with the following lines you can adjust i.e for pps or fps. Yes, there is a builtin DHCP client in the ether dream laser controller but if you run multiple lasers, having a fixed dedicated network makes you focus on laser stuff.

/net/ipaddr 192.168.1.3
/net/netmask 255.255.255.0
/net/gateway 192.168.1.1
/ilda/pps 25000
/ilda/fps 25

Remember to change the EtherIP line in GlobalVars.py

About hardware setup, especially if you have several lasers : ILDA cables are insanely expensive. You may consider the Power Over Ethernet 'POE' option. Buy a very small ILDA cable, a POE splitter and connect everything to the ether dream fixed near your laser. You can have then a simple and very long network cable and use a Power Over Ethernet injector or switch closed to the driving computer. Beware some vendors use 24V POE Injector : POE injectors and splitters must match.


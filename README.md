# Run instructions
The code for this project has been written in Python3.
1. Clone the git repository: ```git clone https://github.com/Tomasvdv/Multi-agent-systems.git```
2. move to the right directory: ```cd Multi-agent-systems/src```
3. Then run the code with: ```python3 demo.py```
<!-- 3. When pushing the 'draw' button, the scene will change (i.e. the plane will fly over the grid cells). -->

<p align="center">
  <img width="460" height="300" src="/img/aircraft.jpg">
</p>

## About the application


<p align="center">
  <img width="600" height="300" src="/img/app.png">
</p>

# Multi-agent-systems Project Report
## Friend or Foe Identification system
### Introduction
This research focuses on analyzing a Friend or Foe Identification System (IFF). Since the invention of radar for localizing enemy planes in WWII, the problem of identifying planes as friend or foe has been around. Because in WW1 the planes were relatively slow and performed more close combat, the planes could be marked with colours to help distinguishing between friends and foes. However, as planes became faster and were flying at higher altitudes, this identification method became obsolete. In WWII the first IFF systems were invented to prevent friendly fire incidents and to aid the overall decision making process in tactical plans. IFF was therefore first used by the military, but the system was later on also used for civilian air traffic.
<br />
Radar-based IFF systems generally consist of a sender that sends a (possibly encrypted) message to a plane. The plane's transponder responds by sending a message back to the sender, which is verified by the sender. The sender can be based on many platforms, e.g. ground defense bases, ships, other planes, etc. IFF systems are only able to positively identify friends. It is not the case (as the name may suggest) that IFF systems are able to positively identify enemy aircraft. 
The latter is due to the fact that the sender can only derive that a plane is friendly if it gets a response back from the plane, but if it doesn't get a response, the plane does not neccessarily have to be a foe. 

### Methods
In this research we will perform multiple exeriments to see how certain parameters setting effect amount of correctly indentified planes. We can change the experiment parameters in two different categories; the envoriment of the simulation itself or the message protocols between agents.
<br />
There are 2 types of agents in the simulated model. Planes and turrets. A plane can either be enemy or friendly w.r.t. the turrets. A turret is a ground based air defense unit that is supposed to shoot down enemy planes that are within its shooting range.

<b>The envoriment: </b>
 1. The amount of turrets in the simulation.
 2. The range of the turrets.
 3. The amount of (friendly) planes in the simulation.
 4. New agents for detecting the planes, while turrets can only shoot the planes.
<br /><br /><b>The message protocols: </b>
 * The amount of messages correctly received can be changed.
 * False information can be inserted to interfere with the simulation.
 * If one category of agents is responsible for detecting the planes and others for shooting different kinds of messages can be tested.
 
#### TCP protocol
TCP labels its packets (bits of information) with numbers. It also uses a deadline before which a packet needs to reach its destination (time-out). For each received packet, the sender is notified by means of an acknowledgment. If a time-out occurs, no acknoledgment is recheived, on which the source sends another copy of the missing/delayed packet. In this way, packets are always assembled in order, without missing packets and in this way the protocol is robust against delays. 
 
### Results

### Discussion
When the core program works as we want it to we have several possible extensions planned for the program.
It might be interesting to split the current turret agent up into two seperate agents: a radar station that can see and identify planes, but can't shoot at them; and a turret that cannot see or communicate with planes, but is able to shoot at planes.

We could also make the simulation more dynamic, by including entry fields for maximal number of planes, maximal number of turrets, turret range and size of the world. This way the simulation doesn't have to be restarted every time the user wants to change some values. 

Another interesting extension would be to expand on or change the communication protocols it uses and the amount of certainty that a turret needs to have before shooting down a plane. 


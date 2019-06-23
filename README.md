# Run instructions
The code for this project has been written in Python3 on Ubuntu.
1. Clone the git repository: ```git clone https://github.com/Tomasvdv/Multi-agent-systems.git```
2. Move to the right directory: ```cd Multi-agent-systems/src```
3. If you don't have Python3 with tkinter install it with:```sudo apt-get install python3-tk ``` 
3.1. Use pip 3 to install: ```sudo pip3 install networkx```and```sudo pip3 install matplotlib```
4. Then run the code with: ```python3 main.py```
<!-- 3. When pushing the 'draw' button, the scene will change (i.e. the plane will fly over the grid cells). -->

<!--
<p align="center">
  <img width="460" height="300" src="/img/aircraft.jpg">
</p>
-->

## About the application
When running instructions above, you will be shown the main interface of the application as shown in the image below. The left panel is used for user interaction with the application model in the background. The middle panel shows the planes and the turrets (see Project Report below for a description of both), the shooting and message sending range of the turrets, and connections between the turrets. The panel on the right is used to get information from the model, like statistics, the knowledge base of a specific turret, or the history of messages sent between a turret and a plane. The application panels will be discussed in more detail below. 

<p align="center">
  <img width="800" height="300" src="/img/app.png">
</p>

### Right panel
This panel is used for interaction between the user and the model. Most important are the *play, pause and step button* on the bottom of the panel. The *play* button lets the simulation run with the speed defined above in the *simulation speed* box. The *pause* button does what it says. And the *step* button lets the simulation run for one step at a time. 
<br />
There are a few entry fields.
1. *Number of planes*: adjusts the number of planes in the simulation. However, for simplicity it is advised to use only 1 plane.
2. *Number of turrets*: adjusts the number of turrets in the simulation. 
3. *Turret range*: adjustst the range of the turrets.
4. *Turret confidence threshold*: the number of turrets that must agree on shooting down a plane before shooting. 
5. *Number of epochs*: the amount of steps that a plane can live.
6. *Failure probability*: the probability that sending a message fails (e.g. message gets lost).  
7. *Simulation speed (iter/second)*: adjusts the speed of the simulation when run with the *play* button. 

### Middle panel
In the middle panel the turrets and planes are shown. The turrets have connections between them (black lines). The message sending and shooting range of the turrets is shown as a black circle (these distances are equal for simplicity). The turret names are printed in blue. The planes can either be friendly or enemy. The change of spawning a friendly plane is 25%. The name of a plane is printed in red for enemy planes, and in lime-green for friendly planes.

### Left panel
In the left planel information about the model can be requested. There are 3 buttons at the bottom of the panel. 
1. *Show statistics*: shows the overall statistics of the model over all epochs until so far. 
2. *Show knowledge base*: shows the knowledge base of a particular turret. First select this button, then click on a turret to view its knowledge base at that moment. The knowledge base is cleared after a run (i.e. the plane has crashed or the plane has been destroyed). 
3. *Show messages*: Shows the messages for all turrets sent for a particular run. 

# Multi-agent-systems Project Report
## Friend or Foe Identification system
### Introduction
This research focuses on analyzing a Friend or Foe Identification System (IFF). Since the invention of radar for localizing enemy planes in WWII, the problem of identifying planes as friend or foe has been around. Because in WW1 the planes were relatively slow and performed more close combat, the planes could be marked with colours to help distinguishing between friends and foes. However, as planes became faster and were flying at higher altitudes, this identification method became obsolete. In WWII the first IFF systems were invented to prevent friendly fire incidents and to aid the overall decision making process in tactical plans. IFF was therefore first used by the military, but the system was later on also used for civilian air traffic.
<br />
Radar-based IFF systems generally consist of a sender that sends a (possibly encrypted) message to a plane. The plane's transponder responds by sending a message back to the sender, which is verified by the sender. The sender can be based on many platforms, e.g. ground defense bases, ships, other planes, etc. IFF systems are only able to positively identify friends. It is not the case (as the name may suggest) that IFF systems are able to positively identify enemy aircraft. 
The latter is due to the fact that the sender can only derive that a plane is friendly if it gets a response back from the plane, but if it doesn't get a response, the plane does not neccessarily have to be a foe. 

We decided to build an aplication using Python3 to simulate an anti-aircraft system which uses a very simplified version of the IFF system to determine if an incoming plane is friend or foe. In our application we decided to model a version of the A1 protocol between anti-aircraft systems (turrets) and an incoming plane. With our application we want to experiment with how the interal settings of the simulation influence the overall misclasification rate of friendly planes. The main research question is: How many friendly planes will be misclassified as enemy and which factors led to this misclassification? In the methods section all internal mechanism will be explained w.r.t the interal knowledge of an agent about the world and how this knowledge expands during the simulation. Also the message protocol we implemented will be discussed with an example how these message lead to a certain conclusion within the knowledge base of the agent. One other element is the influence of the different simulation parameters on the knowledge of an agent about the world. 

### Methods
First we are going to explain the core mechanism generating agents, the knowledge which can be aquired by those agents and the message system which enables the agents to share their knowledge with other agents.
#### Agents
In our simulation we have to types of agents, namely planes and turrets. Before we explain the specifics about our implementation of planes and turrets we need to explain the basic knowledge and message system first.

Each agent has it own list of sent messages, received messages and an inbox. At every epoch of the simulation an agent will check its inbox and perform the following action for each message in its inbox:
* Add the content of the message to its knowledge base
* Add the message to its list of received messages
* Add the message to a message manager for display in the application
* Send a reply to the sender
The reply routine works as follows:

* In case of our implementation of A1 the reply will be: K_agent1(message)
* This reply is added to the agents knowledge base
* If it is the case that K_a(K_b(K_a(K_b(message)))) set the message as confirmed
* Else sent back replies until it is the case that K_a(K_b(K_a(K_b(message))))

After all messages in the inbox are handled the agent will check whether one of its previous messages hasn't reached the other agent yet. It will resend all messages which aren't confirmed yet.

<b>Turret</b>

At initialization each turret will send its position to other turrets. This will ensure its common knowledge for the turrets were each turret is relative to a plane and to enable a different turret to order another turret to fire when a plane is close.
Each turret has also a specific range in which it can spot planes. 
During the simulation the turret will keep track of each plane in its own range. If it is not encountered before by the turret it will first broadcast the planes position to the other turrets. It will sent a message to the plane to identify itself.

When it is the case the plane has been encountered before, the turret will update its knowledge about how long the plane is already in sight.
Next the turret will loop through its received messages and if one message is from a plane and it contains the message "key" and its name, the turret will add to its knowledge he knows that plane is friendly.


In this research we will perform multiple exeriments to see how certain parameters setting effect amount of correctly indentified planes. We can change the experiment parameters in two different categories; the envoriment of the simulation itself or the message protocols between agents.
<br />
There are 2 types of agents in the simulated model. Planes and turrets. A plane can either be enemy or friendly w.r.t. the turrets. A turret is a ground based air defense unit that is supposed to shoot down enemy planes that are within its shooting range.

<b>The envoriment: </b>
 1. The amount of turrets in the simulation.
 2. The range of the turrets.
 3. The amount of (friendly) planes in the simulation.
 4. <!-- New agents for detecting the planes, while turrets can only shoot the planes. -->
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


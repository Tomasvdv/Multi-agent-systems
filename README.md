# Running instructions
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

### Left panel
This panel is used for interaction between the user and the model. Most important are the *play, pause and step button* on the bottom of the panel. The *play* button lets the simulation run with the speed defined above in the *simulation speed* box. The *pause* button does what it says. And the *step* button lets the simulation run for one step at a time. 
<br />
There are a few entry fields.
1. *Number of planes*: adjusts the number of planes in the simulation. However, for simplicity it is advised to use only 1 plane.
2. *Number of turrets*: adjusts the number of turrets in the simulation. 
3. *Turret range*: adjusts the range of the turrets.
4. *Turret confidence threshold*: the number of turrets that must agree on shooting down a plane before shooting. 
5. *Number of epochs*: the amount of steps that a plane can live.
6. *Failure probability*: the probability that sending a message fails (e.g. message gets lost).  
7. *Simulation speed (iter/second)*: adjusts the speed of the simulation when run with the *play* button. 

### Middle panel
In the middle panel the turrets and planes are shown. The turrets have connections between them (black lines). The message sending and shooting range of the turrets is shown as a black circle (these distances are equal for simplicity). The turret names are printed in blue. The planes can either be friendly or enemy. The chance that a spawned plane is friendly is 25%. The name of a plane is printed in red for enemy planes, and in lime-green for friendly planes. When a plane is marked to be shot down the next epoch by a turret, a red line will be drawn from the turret to the plane.

### Right panel
In the left panel information about the model can be requested. There are 3 buttons at the bottom of the panel. 
1. *Show statistics*: shows the overall statistics of the model over all epochs until so far. 
2. *Show knowledge base*: shows the knowledge base of a particular turret. First select this button, then click on a turret to view its knowledge base at that moment. The knowledge base is cleared after a run (i.e. the plane has crashed or the plane has been destroyed). 
3. *Show messages*: Shows the messages for all turrets sent for a particular run. 

# Multi-agent-systems Project Report
## Identification Friend or Foe system
### Introduction
This research focuses on analyzing an Identification, Friend or Foe (IFF) System. Since the invention of radar for localizing enemy planes in WWII, the problem of identifying planes as either friend or foe has been present. In WW1 the planes were relatively slow and performed nearly exclusively close quarters combat (dogfights) and no targeted strikes, the planes could be marked with colours to help pilots distinguish enemy planes from friendly planes. However, as planes became faster, started flying at higher altitudes, and the range of their weapons increased, this identification method became obsolete. In WWII the first functional IFF systems were invented and put into use to prevent friendly fire incidents and to aid the overall decision making process in tactical plans. IFF was therefore originally developed and used by the military, and only later adapted and put in use for civilian air traffic.
<br />
Radar-based IFF systems generally consist of a sender that sends a (possibly encrypted) message to a plane, often called a challenge. The plane's transponder responds by solving the challenge (i.e. determining the correct response) and sending a response back to the sender, which is then verified by the sender. The sender can be based on many platforms, e.g. ground defense bases, ships, other planes, etc. IFF systems are only able to positively identify friendly units. It is not the case (as the name may suggest) that IFF systems are able to positively identify enemy aircraft. 
The latter is due to the fact that the sender can only derive that a plane is friendly if it gets a response back from the plane, but if it doesn't get a response, the plane does not necessarily have to be a foe. It could be that something went wrong during the sending or receiving of the message.

We decided to build an application using Python3 to simulate an anti-aircraft system which uses a very simplified version of the IFF system to determine if an incoming plane is friend or foe. In our application we decided to model both a version of the A1 protocol (as in the LOK-web assignment) and the Transmission Control Protocol (TCP) between anti-aircraft systems (turrets) and an incoming plane. With our application we want to experiment with how the internal settings of the simulation influence the overall misclassification rate of friendly planes. 

The main research question is: How many friendly planes will be misclassified as enemies and which factors led to this misclassification?

In the methods section all internal mechanism will be explained w.r.t. the internal knowledge of an agent about the world and how this knowledge expands during the simulation. In addition, the message protocol we implemented will be discussed with an example of how these messages lead to a certain conclusion within the knowledge base of the agent. One other element is the influence of the different simulation parameters on the knowledge of an agent about the world. 

### Methods
<!-- First we are going to explain the core mechanism generating agents, the knowledge which can be acquired by those agents and the message system which enables the agents to share their knowledge with other agents. -->
In this section, the core mechanisms of the simulation will be discussed. This includes the way messages are passed in the simulation and the different kinds of knowledge that agents can acquire over the course of the simulation.

<!--Before we explain the specifics about our implementation of planes and turrets we need to explain the basic knowledge and message system first.-->
#### Message protocol
All agents communicate to each other using messages. Messages are marked as successfully received through either the A1 or the TCP protocol.
Every message that is send has a chance of not reaching its destination. This probability can be set using the left command panel in the simulation. 

Each agent has it own list of sent messages, received messages and an inbox. At every epoch of the simulation an agent will check its inbox and perform the following action for each message in its inbox:
* Add the contents of the message to its knowledge base
* Add the message to its list of received messages, along with a note on who has sent the message
* Add the message to a message manager for display in the application
* (Optionally) send a reply to the sender to confirm that the message was received successfully.

After all messages in the inbox are handled the agent will check whether one of its previous messages hasn't reached the other agent (i.e. it hasn't received a confirmation). It will resend all messages which aren't confirmed yet.

##### A1
In the protocol A1, all agents reply to each message they receive with the fact that the contents of the message are now known by the agent. This continues until K_a(K_b(K_a(K_b(message)))) holds true in the model. 

The A1 protocol works as follows:
* Assume that the sender is called a, and the receiver is called b.
* a sends a message to b. The contents are 'message'
* The reply of agent b to agent a will be: K_b(message). This means that message is known to b.
* If the reply is successfully received by agent a, K_a(K_b(message)) will be added and send back to agent b.
* In the case that a message does not reach the receiving agent, the message will be resent the next epoch. 
* This process is repeated until  K_a(K_b(K_a(K_b(message)))) is true in the model
* If it is the case that K_a(K_b(K_a(K_b(message)))), agent a can set the message as successfully received.


##### TCP
The TCP protocol is a bit simpler than the A1 protocol. This is due to the protocol only requiring one confirmation per message sent. This confirmation is called an ack (short for acknowledgement). For every message that is received, the receiving agent replies with an ack message. If an ack is not received within a set amount of time, the sender will assume that something went wrong and resend the packet. 

An interesting aspect of TCP is that it numbers the messages it sends. This is due to the protocol originally being used for transferring packets of data over the internet. By numbering the packets, the original datastream can be reconstructed by ordering the packets in the right order. As this is not necessary in our system, the explicit numbering of messages has been omitted and is instead done implicitly in the system.

The protocol can be summarized as follows:
* Again, a and b are agents
* a sends a message to b. The contents are 'hello'
* b replies to a, ack(hello)
* If the ack is received, a sets the message as being successfully received. 
* If the ack is not received, a resends the initial message to b again.
* This continues until all of a's messages are labeled as successfully received.

The TCP protocol is much faster than the A1 protocol, as b doesn't explicitly have to know that a has successfully received its replies. As all messages only contain facts that are sent from agent to agent duplicate facts won't make a difference in the resulting knowledge base and due to the implementation the knowledge base won't contain any duplicates, so there are no risks in receiving a message twice.


#### Agents
The simulation consists of two different types of agents; planes and turrets. Turrets can send challenges to planes and can communicate with other turrets on the contents of their knowledge base. <!--This will be elaborated on in more detail further on in the paper.-->

##### Turrets
During the first epoch of the simulation each turret will send its position in the world to other turrets. This will ensure that it's common knowledge among all turrets where each turret is located. This allows turrets to calculate which turret is closest to a plane and therefore is best suited to shoot down the plane if it is identified as an enemy.

Each turret has also a specific range in which it can spot planes. This is indicated in the simulation as a circle around the turret.
During the simulation the turret will keep track of all planes that enter its range. If it is not yet detected or identified by any of the other turrets it will broadcast the position of the plane to the other turrets. It will then send a message to the plane ordering it to identify itself.

When it is the case the plane has been encountered before, the turret will update its knowledge about how long the plane is already in sight and how many messages it has ignored (or not received).
Next the turret will loop through its received messages and if one message is from a plane and it contains the message "key" and its name, the turret will add to its knowledge the fact that the plane is friendly, and broadcast this knowledge to the other turrets.

If the plane ignores enough messages sent by the turret, the turret will mark the plane as not friendly.

The turret can decide to trigger the shooting procedure if the following three facts are true in the model:

* The plane hasn't responded for a set number of epochs
* It is the case the plane is not known as friendly
* The plane has been in sight for too long.
* A set number of turrets marked the plane as probably not friendly.

When the turret decides its time to shoot it will loop through all turrets locations and determines the closest turret relative to the plane. It will then send a message to the turret ordering it to shoot down the plane.

In the next epoch of the simulation the turret receiving the message will shoot down the plane if the message was correctly received and the plane is still in range of the turret.

<!--open fire if it knows it needs to shoot down the plane and if it is the case the confidence threshold of number of turrets which identifies the plane as foe has been met.-->

##### Planes
On initialization a plane is given a location the border of our simulation world. It will receive a constant speed of one tile per epoch of the simulation. It flies in a straight line until it either reaches another border of the simulation, or it is shot down by one of the turrets.

When a plane receives a message from a turret asking it to identify itself, it saves this in its knowledge base.
If a plane has "identify" in its knowledge base and the plane is friendly, it will sent a response to the turret that asked the plane to identify itself containing the word friendly. This functions as an abstraction of successfully solving a challenge sent by the turret. If the plane is not friendly it will sent the message: 'no response' to the turret. This message is used as a practical implementation of not getting a reply from the plane.

#### Experiment settings

In this research we will perform multiple experiments to see how certain parameters setting affect the number of correctly identified planes. 

The following data points will be measured in the simulation:
* Total of planes generated
* Friendly planes generated
* Enemy planes generated
* Friendly planes in range
* Enemy planes in range
* Friendly planes shot max epochs
* Enemy planes shot no response
* Enemy planes shot max epoch counter

In each experiment there will be 1000 planes generated in total. The amount of planes in range versus the reason it got shot down will serve as a measurement of the simulation performance.

Three different experiments will be done which will test different settings of the simulation.
In the settings below, turret confidence threshold denotes the amount of turrets that need to mark a plane as an enemy before it can be shot down. The number of epochs parameter denotes the number of epochs that need to be passed without a plane sending a response to a turret before it can be marked as an enemy by a turret.
Failure probability denotes the probability that a message is not delivered to its recipient.

Settings for the experiment on number of epochs: 
* Number of planes 1
* Number of turrets 3
* Range of turrets 4
* Turret confidence threshold 1
* Number of epochs before shot: [8,4]
* Failure probability: 0.1


Settings for the experiment on the turret confidence threshold: 

* Number of planes 1
* Number of turrets 3
* Range of turrets 4
* Turret confidence threshold [1,2,3]
* Number of epochs before shot: 8
* Failure probability: 0.1

Settings for the experiment on Failure probability: 

* Number of planes 1
* Number of turrets 3
* Range of turrets 4
* Turret confidence threshold 1
* Number of epochs before shot: 8
* Failure probability: [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

The simulation speed was set high (> 1000) to generate results quickly. 


### Results
The results for the experiments are shown in the barplots below. These are the results (from top to bottom respectively) for the experiments on the amount of epochs a plane is allowed to pass without sending a response (it will then be marked as 'enemy'), the confirmation threshold (i.e. by how many turrets a plane must be marked as 'enemy' before being shot at) and the message fail probability (the probability that sending a message fails, e.g. because the message was lost or corrupted). The legend positioned on the right side of the barplots first lists the used protocol (A1 or TCP) and then the type of plane. The results are given in the amount of shot down planes over the amount of planes that were in range of a turret. 
<p align="center">
  <img width="500" height="300" src="/img/epochs.png">
</p>
<p align="center">
  <img width="500" height="300" src="/img/threshold.png">
</p>
<p align="center">
  <img width="500" height="300" src="/img/message_fail.png">
</p>


### Conclusion and discussion
With regard to the number of epochs, there is no significant difference between the A1 and TCP protocol. TCP outperforms A1 when the number of epochs is low (4 in the barplot), and A1 outperforms TCP when the number of epochs is high (8 in the barplot). The TCP protocol is faster than the A1 protocol. Therefore, when the plane is allowed little epochs to finish its protocol with a turret, the turret may not be able to identify the plane as friendly in time, and will shoot at the plane as a result. When given more epochs to finish its protocol, A1 performs allows for a situation in which friendly planes are never shot down. The same reasoning seems to hold for the result of the enemy planes.
<br />
When looking at the confirmation threshold (the amount of turrets that must agree on shooting down a plane before it is shot down) we see that in general the number of friendly planes that are shot decreases as the confirmation threshold increases. This is easily explained by the fact that it is 'more certain' that a plane is an friend or foe when multiple turrets gave the same label to a plane. An interesting result is that the percentage of shot down friendly planes for the A1 protocol (red bar) is almost 0 for a threshold of 1 and 3, and around 10% for a threshold of 2. One would expect higher friendly plane kills for a threshold of 1. There is no straightforward explanation for this result. Moreover, we observe that the amount of shot enemy planes also decreases as the confirmation threshold increases. So the results show that there is a tradeoff when setting a higher confirmation threshold: the higher the threshold, less friendly planes will be shot down, but also less friendly planes will be shot down. 
<br />
The message send fail probability results (the probability that sending a message fails, e.g. because the message was lost or corrupted) show in general that the lower the fail probability, the less enemy planes are shot down. This pattern was expected since a higher fail probability in sending messages will result in a longer time needed for the identification of a plane. Moreover, the data shows that TCP results in more kills for both friendly and enemy planes (in most cases). This may be explained by the fact that TCP is a faster protocol, enabeling the turrets to identify planes faster and shoot them down before they fly out of range. 
<br />
In general we can say that the protocol shoots more enemy planes than friendly planes, which is good. However, still quite a lot of friendly planes are shot down. This may be due to the 'number of epochs before shot' parameter which is still a little too low. 


#### The simulation
The simulation turned out very nicely, with a large number of parameters that can be altered to test their influence. The speed at which the simulation executes makes for very easy testing of new settings. The only bottleneck of the system is when a large (bigger than five) number of planes are all flying in the simulation at once, as all turrets keep each other updated on the current state of all planes they see. Overal the simulation works well and we are very pleased with the final product.


#### Future research and possible extensions
There were several interesting extensions that were thought up while working on the project, that could not be included as the scale of the project would become too big. 

One such extension would be to split the current turret agent up into two separate agents: a radar station that can see and identify planes, but can't shoot at them; and a turret that cannot see or communicate with planes, but is able to shoot at planes and has to rely on the radar station to give it commands.

Another interesting extension would be to include a third messaging protocol to the system and see how it compares to the two already in place.

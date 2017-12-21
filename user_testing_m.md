# Main hypotheses 
* Emotional rapport <!-- (we do NOT attempt to prove that this is necessary) -->
	* Movement - Luko's form and motion allows users to build rapport with Luko on an emtional level
	* Sounds - Luko's non-verbal sounds allows users to build rapport with Luko on an emtional level

* Productivity
	* Movement - Luko's 
    * Sounds

# User Testing - Methodology
*to be updated throughout the user testing process*

An overview on:
* Hypotheses to test
  * Experiment to perform
  * Corresponding control experiment
  * Experiment metrics (qualitative/quantitative)
* Participant selection
* Test times/logistics

<br>

## Hypothesis: Gestures to move Luko's gaze aids productivity
* Prove that manually moving a lamp across areas of a desk is cumbersome
* Then prove that this is solved with the point to location feature
* A dynamic task switching between 2 laptops/notebooks placed ~1ft away from each other (tune size)

**Experiment:**
* User performs simple maths calculations on 2 notebooks 1ft away, switching between them for each calculation
* Sensor (phone's ambeint light value was used) value to exceed threshold for the lamp to be determined as having moved to the notebook

Test setup   | Control setup
------------ | -------------
Luko with point to location node active <br> `rosrun cv handrec_v5.py` <br>| A standard desk lamp - 5dof or with flexible neck joint <br> _Possibly Luko with unlocked joints - but must be treated with care_

**Test Metrics:**
* Number of maths problems performed in a 2-minute span

<br>

## Hyptothesis: Non-verbal interaction improves over verbal interaction
_test metrics, experiment yet to be defined_

Test setup   | Control setup
------------ | -------------
Luko with sound engine and voice input nodes active | Amazon Echo Dot

<br>

## Hypothesis: Movement can establish emotional rapport with a user unobtainable by speech
Test setup   | Control setup
------------ | -------------
Luko with normal movement | Luko with delibrately robotic movement

<br>

## Hypothesis: Increases productivity

**Experiment:**
* A suite of tasks which require images to be displayed on the desk
	* eg. drawing an image
	* _more tasks to be defined - some which exploit the fact that a projector can display directly atop a working surface_

Test setup   | Control setup
------------ | -------------
Luko with projection node active | iPad with 'hey siri' active


**Test Metrics:**
* Efficacy scores for each task
* Measure number of subtasks completed within a set time (~2mins)

<br>

## Hypothesis
_Luko mainly expresses through motion, is this less or more distracting than an inanimate voice-based system? 
If so, does the added emotional visual interaction compensate for the distraction?_
* _design a test to possibly explore this_

<br>

## Participant Selection
* Pitch Luko to visitors willing to spend some time testing out Luko 
	* _Science Museum/Exhibition Road?_



Hyp1: tested by making Luko very emotionally aware, and delibrately robotic - surveyed users on how well they seemed to connect with Luko
 - verified

Hyp2: tested by comparing Luko to Alexa - surveyed users on how emotionally connected they felt to both (scores out of 10)
also tested by comparing without sounds - asking people how creeped out they were

Hyp3: Verified, gestures improve on physical movement significantly.
On the x users tested, the number of 'switches' performed across the given desk space was on average 1.5x more than in the case with a standard hinged desk lamp.


##Conceptualization of Luko:
--	Luko to replace standard desk lamps

	-Movement
    	-Emotional rapport
        -Productivity
    -Sound
    	-Emotional rapport
        
	-Emotional rapport (we do NOT attempt to prove that this is necessary)
    	-Movement
        -Sounds
    -Productivity
    	-Movement
        -Sounds
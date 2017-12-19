# User Testing - Methodology
*to be updated throughout the user testing process*

An overview on:
* Hypotheses to test
  * Experiment to perform
  * Corresponding control experiment
  * Experiment metrics (qualitative/quantitative)
* Participant selection
* Test times/logistics


## Hypothesis #1: Gestures to move Luko's gaze aids productivity
* Prove that manually moving a lamp across areas of a desk is cumbersome
* Then prove that this is solved with the point to location feature

**Experiment:**
* A dynamic task switching between 2 laptops/notebooks placed ~1ft away from each other (tune size)
	* constrain task such that lamp must face workspace
	* _exact task yet to be defined_

Test setup   | Control setup
------------ | -------------
Luko with point to location node active <br> `rosrun cv handrec_v5.py` <br>| A standard desk lamp - 5dof or with flexible neck joint <br> _Possibly Luko with unlocked joints - but must be treated with care_

**Test Metrics:**
* Efficacy scores for each task
* Measure number of subtasks completed within a set time (~2mins)

## Hyptothesis #2: Non-verbal interaction improves over verbal interaction
_test metrics, experiment yet to be defined_

Test setup   | Control setup
------------ | -------------
Luko with sound engine and voice input nodes active | Amazon Echo Dot

## Hypothesis #3: Embedded projection system increases productivity
* Prove the need for a built-in pico projector

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

## Hypothesis #4
_Luko mainly expresses through motion, is this less or more distracting than an inanimate voice-based system? 
If so, does the added emotional visual interaction compensate for the distraction?_
* _design a test to possibly explore this_


## Participant Selection
* Pitch Luko to visitors willing to spend some time testing out Luko 
	* _Science Museum/Exhibition Road?_
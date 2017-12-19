# User Testing - Methodology
*to be updated throughout the user testing process*

An overview on:
* Participant selection
* Hypotheses to test
  * Experiment to perform
  * Corresponding control experiment
* Experiment metrics (qualitative/quantitative)

## Hypothesis #1: Gestures to move Luko's gaze aids productivity
* Prove that manually moving a lamp across areas of a desk is cumbersome
* Then prove that this is solved with the point to location feature

**Experiment:**
* A dynamic task switching between 2 laptops/notebooks placed ~1ft away from each other (tune size)
	* constrain task such that lamp must face workspace

Test setup   | Control setup
------------ | -------------
Luko with point to location node active <br> `rosrun cv handrec_v5.py` <br>| A standard desk lamp - 5dof or with flexible neck joint <br> _Possibly Luko with unlocked joints - but must be treated with care_

**Test Metrics:**
* Measure number of subtasks completed within a set time (~2mins) 

## Hyptothesis #2: Non-verbal interaction improves over verbal interaction
_test metrics, experiment yet to be defined_

Test setup   | Control setup
------------ | -------------
Luko with sound engine and voice input nodes active | Amazon Echo Dot


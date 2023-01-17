# Problem description
## Background: 
Prior to traveling to a radio installation site to perform field maintenance, a check of 
the position of the Radio Resource Unit (RRU) on the mast is needed. In this way, the 
crew knows the correct equipment to bring. Failing to do so incurs the cost of a 
second trip. In many cases, a photo of the location is available, but the time to find 
and look at the photo also incurs a cost.
##  Problem Statement:
The idea is to develop an image processing machine learning model that 
identifies the positioning of an RRU on a mast based on a photo.
## Solution Expectation:
Provide a script that , given a photo of an RRU, can identify if the RRU is on the 
ground or at the top of the mast. The goal is to reach 70-75% accuracy.




# Deep Classifier Project

## workflow
1. Update config.yaml
2. Update secrets.yaml [Optional]
3. Update params.yaml
4. Update the entity
5. Update the configuration manager in src config.
6. Update the components
7. Update the pipeline
8. Test run pipeline stage
9. run tox for testing your package
10. Update the dvc.yaml
11. run "dvc repro" for running all the stages in pipeline

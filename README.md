# 06aa7e1e-ebc4-48c4-bff0-b794abdc7060
https://sonarcloud.io/summary/overall?id=examly-test_06aa7e1e-ebc4-48c4-bff0-b794abdc7060

## Heat Wave Model
Steps to Run the model

Best model --> Federated Conv1D Model 

1)  The main performing model has been provided in the folder labeled models uner heat wave 
2)  basic load procedure for the model would to use load_model function from keras to laoad the directory
3)  the input to the fed conv1d model will be an 1d array of past 256 days of min and max temp
4)  the output would be an array of size 365 days i.e the next 365 days 
5)  runner.ipynb contains the model building and model training code that is utilizing the caller_2.py utils file 
6) test.ipynb contains the code that would create the dataset for year 2022 which will be fed into the model for the yearly prediction of 2023

Note--> Due to limited computation availabilty we were not able to run the Federated model for more epochs 

Also the other 3 reference model were too big to be uploaded on github so we have shared a model_links.txt file in the heatwave folder that contains all the refrence
model we have build that includes  Fedearted Conv2D Model , Centralized Conv1D model, Centralized Conv2D model 
Each model folder has been equipped with its runner and testing function with its output in the output folder


## AQI Model

Best model -> multi_multi_CNN ( Multi-headed Conv-1D model)

In the model.ipynb file replace the path_csv with the any dataset and run the required cell to get the 2023 predicted AQI value.

All the AQI models have provided in the 'AQI/models' folder.

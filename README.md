# azure-serverless-template


The goal of this project was to create a template for a Serverless RESTful API in Python using Azure. 
It should have CRUD endpoints and persistence of data. 


| Component  | Type  | Service  |
|---|---|---|
|  Interface |  Algorithm | Database  |
|  API | Function  |  CosmosDB |


Run locally:

func host start

Push changes:

func azure functionapp publish templateitem --build-native-deps


Reference:


[Create Your First Function](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python)
- Read **[Azure Web Apps](https://azure.microsoft.com/en-us/services/app-service/web/)**.
- Install **[Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=linux%2Cpython%2Cbash#v2)**
  
1. Set application settings according to its configuration specification 
`az webapp config appsettings set --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true ...`  

2. Deploy Azure Web application
`az --% webapp up --runtime "PYTHON|3.8" --name ml-search-api-goods-dev`

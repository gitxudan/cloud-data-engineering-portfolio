# Azure Event-Driven Data Pipeline

## Overview
This project simulates clickstream data flowing into Azure Event Hub and processed by Azure Function App.  
It demonstrates building an end-to-end event-driven data pipeline on Azure.

## Folder Structure
- `simulator/` → Data generators  
- `src_azure-function/` → Function App code  
- `architecture/` → Architecture diagrams  
- `sample-data/` → Example JSON data  

## How to Run
1. Copy `.env.example` → `.env` and fill in your Azure keys.  
2. Run simulator scripts to generate events.  
3. Start Azure Function locally (`func start`) or deploy to Azure.  
4. Check output in CosmosDB.

## Technologies
Azure Event Hub | Azure Function App | CosmosDB | Python
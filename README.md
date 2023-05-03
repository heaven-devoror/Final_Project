## Table of contents
- [Project Purpose](#project-purpose)
- [Dataset Structure](#dataset-structure)
- [Technology Used](#technology-used)
- [Step by step procedure](#step-by-step-procedure)
- [Dashboard](#dashboard)
- [Further improvements](#further-improvements)

## Project purpose
We are going to use Global Power Plant data from [power_plant_data](https://datasets.wri.org/dataset/globalpowerplantdatabase).
We are going to find countries with the most energy sources and power generation capacity.

## Dataset structure

Column Name                   | Data Type | Definition
-----------                   | ----------| -------------
country                       | String    | Country name abbreviation
country_long                  | String    | Full Country name
name                          | String    | Power plant name
gppd_idnr                     | String    | 10 or 12-character identifier for the power plant
capacity_mw                   | DOUBLE    | Electrical generating capacity in megawatts
latitude                      | DOUBLE    | Geolocation in decimal degrees
longitude                     | DOUBLE    | Geolocation in decimal degrees
primary_fuel                  | String    | Energy source used in electricity generation or export
other_fuel1                   | String    | Energy source used in electricity generation or export,
other_fuel2                   | String    | Energy source used in electricity generation or export
other_fuel3                   | String    | Energy source used in electricity generation or export
comm_year                     | String    | Year of plant operation, weighted by unit-capacity when data is available
owner                         | String    | Majority shareholder of the power plant
source                        | String    | Entity reporting the data; could be an organization, report, or document
url                           | String    | Link corresponding to the "source" field
wepp_id                       | Stirng    | Attribution for geolocation information
yr_cap_data                   | DOUBLE    | Year the capacity information was reported
genration_gwh_2013            | DOUBLE    | Electricity generation in gigawatt-hours reported for the year 2013
genration_gwh_2014            | DOUBLE    | Electricity generation in gigawatt-hours reported for the year 2014
genration_gwh_2015            | DOUBLE    | Electricity generation in gigawatt-hours reported for the year 2015
genration_gwh_2016            | DOUBLE    | Electricity generation in gigawatt-hours reported for the year 2016
genration_gwh_2017            | DOUBLE    | Electricity generation in gigawatt-hours reported for the year 2017
genration_gwh_2018            | DOUBLE    | Electricity generation in gigawatt-hours reported for the year 2018
genration_gwh_2019            | DOUBLE    | Electricity generation in gigawatt-hours reported for the year 2019
generation_data_source        | String    | attribution for the reported generation information
estimated_generation_gwh_2013 | String    | Estimated annual electricity generation in gigawatt-hours for the year 2013
estimated_generation_gwh_2014 | String    | Estimated annual electricity generation in gigawatt-hours for the year 2014
estimated_generation_gwh_2015 | String    | Estimated annual electricity generation in gigawatt-hours for the year 2015
estimated_generation_gwh_2016 | String    | Estimated annual electricity generation in gigawatt-hours for the year 2016
estimated_generation_gwh_2017 | String    | Estimated annual electricity generation in gigawatt-hours for the year 2017
estimated_generation_note_2013| String    | label of the model/method used to estimate generation for the year 2013 
estimated_generation_note_2014| String    | label of the model/method used to estimate generation for the year 2014
estimated_generation_note_2015| String    | label of the model/method used to estimate generation for the year 2015
estimated_generation_note_2016| String    | label of the model/method used to estimate generation for the year 2016
estimated_generation_note_2017| String    | label of the model/method used to estimate generation for the year 2017

## Technology used
- Cloud - GCP
- Infrastructure as code (IAC) - Terraform
- Workflow orchestration - Prefect
- Data warehouse - Bigquery
- Data Transformation - DBT
- Data visualization - Google Looker Studio

## Step by step procedure
We are going to use GCP VM on Ubuntu 22.04 LTS in Google cloud. This will require a goolge cloud account and service account for appropriate permission.

1. Visit Google Cloud Console [link](https://console.cloud.google.com/) and create google cloud account
2. Create [Project](https://console.cloud.google.com/cloud-resource-manager)
3. Setting Service Acount Access: 
    * Go to IAM Roles for service account [IAM&Admin](https://console.cloud.google.com/iam-admin/iam)
    * Click the Edit principal icon for your service account.
    * Add these roles in addition to Viewer : Storage Admin + Storage Object Admin + BigQuery Admin
4. Create a service [account key](https://cloud.google.com/iam/docs/keys-create-delete#creating):
    * Download the JSON credentials and save it, e.g. `~/.gc/<credentials>`
```
    export GOOGLE_APPLICATION_CREDENTIALS=<path_to_your_credentials>.json
    gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
    gcloud auth application-default login
```
5. Create a [VM instance](https://console.cloud.google.com/compute)

6. On your VM, clone the repo, git clone https://github.com/mikecolemn/mpls-311-data.git, and then cd into the repo folder

7. Run the file in setup folder and press "yes" when asked and when in terraform enter you Project ID:
```bash
bash setup_file.sh
```

8. Create conda enviroment
```bash 
conda create -n final python=3.9
```

9. Activate the enviroment
```bash
conda activate final
```

10. Install Dependencies
```bash
pip install -r requirements.txt
```
11. Setting up prefect cloud
- Sign up for Prefect [cloud](https://app.prefect.cloud/)
- Create a Workspace. Then go to blocks. Add block GCS bucket. Then Enter the name of your GCS bucket.
- Add GCP credentials block and add your JSON credential file data in it.

12. Execute your main.py file
```bash
python main.py
```

## Dashboard
You can access the dashboard from [here](https://lookerstudio.google.com/reporting/f11e7d6b-441f-4182-a23b-04d49e0a6112)

## Further improvements
- Create a CI/CD pipeline to automate the deployment of the data pipeline
- Use Prefect Cloud to schedule weekly processing
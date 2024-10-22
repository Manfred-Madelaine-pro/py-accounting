<img src="img/logo.png" align="right" />

# :classical_building: Accounting 

Aim is to propose a simple algorithm that read, parse, store, process and display financial data for individuals :money_with_wings:.


## :tada: Examples

<details>
<summary>Example in old version (Click to expand)</summary>

![running main script](img/main.PNG)

</details>

## :spiral_calendar: Dates

### :rocket: Version 2 Started 
Project pitched and started the _11th december 2020_

### :dart: Release date 
- First expected release the friday **15th december 2020** 
- Second expected release the **10th january 2021** 


## :electric_plug: Dependencies
1. :desktop_computer: Set your Virtual Environment:

    ``` bash
    # Download venv librairy
    apt-get install python3-venv -y
    # Create your venv
    python3 -m venv venv
    # Activate your venv
    . venv/bin/activate
    ```
    
    _For more information, go to [Python Virtual Environment Official Documentation](https://docs.python.org/3/library/venv.html)._

1. :package: Install the project dependencies:

    ``` bash
    apt install python3-pip
    pip install PTable
    pip install Flask
   
	pip install PyPDF2
    ```


## :zap: Quick start

1. Database configuration:

	``` bash
		mkdir -p back/database/ && touch back/database/accounting.db
		mkdir -p data/sg/ 
 		# create the input directory for file integration
    ```

1. To start the backend server, simply run bellow commands:

	``` bash
		export FLASK_APP=controller.py
		export FLASK_ENV=development
		flask run
		# * Running on http://127.0.0.1:5000/
	```


## :art: Architecture

### Version 2
![Accounting Architecture](img/accounting_diagram.png)

<details>
<summary>Version 1 (Click to expand)</summary>

![Accounting Architecture](img/accounting_diagram_flat.png)
 
</details>


## :clipboard: Tasks

1. Database
	- [x] Create schema
	- [ ] Try to use some DB framework
	- [ ] Fix the duplicate issue
	
1. Payments
	- [x] Create account
	- [x] Fake few payments
	- [x] Compute few metrics
	  
1. REST API
	- [x] Expose data 
		- [x] Flask
		- [x] GraphQL ~> not very effective
	- [x] Design API (Postman ~> not effective)
	- [ ] Insert payments ?
	  
	- [ ] Expose metrics
	  
1. Integration
	- [x] CSV from Societe Generale
	  - [x] Get all files in directory
	  - [x] read each file, one after the other
	  - [x] Parser rows and map to RawPayments
	- [x] Save in database
		- [x] Generic object's management in database
		- [x] If file is duplicate => skip
	- [ ] View all payments and duplications between files (count same lines in file and across files)
	- [ ] CSV from N26
	- [ ] 4% of the database (72/1685 payments) is corrupted by duplicated values from different files

1. Statistics
	- [x] Low level stats
	  - [x] Total credit/debit for quantity and amount
	  - [x] Min, Max, Avg, opening, closing
	- [x] Handle consumption periods (~daily, weekly, monthly)
	  	- [ ] Add periodicity: Trimester, Semester
	- [ ] Metrics column info
		- [ ] Add header info line for metrics column
		- [ ] Add footer avg line for metrics column
	- [ ] Identify FIXED income and expenses (try to rely on LABELS)
	- [ ] Define profile
	- [ ] string similarity calculation to identify recurrent transactions 
	  
1. Filter v2
   - [ ] Allow labeling (Add, remove, reset)
   - [ ] Auto labeling on token 
	   - [ ] Available labels: transport, rent, salary, phone, AMZ, SG, Healthcare...
   - [ ] Filter payments on account & list of labels 
   - [ ] Ensure payments uniqueness
   - [ ] Group some labels together (expose groups to client ?) 
   - [ ] Filter payments on account & group
   - [ ] Percentage of payments (qty & amount) labeled (or group) for a given period
   - [ ] Pie chart for example
	
	<details>
	<summary>Filter v1 (Click to expand)</summary>
	
	1. Labels
		- [ ] Tag all payments 
		- [ ] Define groups based on tags
		- [ ] Create groups that matches perfectly one tag, multiple tags or other groups 
		- [ ] Apply metrics on groups
		- [ ] Allow enforced new tag for payment id
	
		- [ ] Count payments in groups
		- [ ] Count payments untagged 
		- [ ] Identify overlapping tags
		  
		- [ ] Auto labeling on rules
		- [ ] Endpoint for labeling
		- [ ] Create categories and pattern that fall in this category
			- [ ] Courses
			- [ ] Amazon
		- [ ] Can 2 categories share same payments ?
			- [ ] Need exclusive categories for global expenses pie-chart
			- [ ] and non-exclusive 

   </details>
	
1. Integrate PDFs
   - [x] Download all PDFs available from banking platforms
   - [ ] Read Parse (PyPDF2, tabula)
   - [ ] Extract data ~> not very effective
   - [ ] Store raw payments

1. Architecture
	- [ ] Design first diagram of internal services
	  - [ ] Try coding schema
	- [ ] Add the schema to README 
	- [ ] Define API specification using Swagger
   
1. Front
	- [ ] Consumption map on a calendar just like github contribution calendar
	- [ ] Display payments curve


## :joystick: More examples

### :floppy_disk: Database example 

![Database example](img/database_example.png)
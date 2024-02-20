# RainAU
[toc]
## Description
The data is from https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package/data. This dataset contains about 10 years of daily weather observations from many locations across Australia.  
This website is used to predict next-day rain in Australia, and provide downloadable temperature comparison charts, as well as comparison charts of rainfall and evaporation, to visitors.  

## Cloud Deployment
The current-version project has been deployed to AWS.  
http://hiwaperth.com/

## Technology choice
Python  
Mysql  
Django  
HTML+CSS+Bootstrap+Echart+JS  

## Local Environmental deploy
**1. Install MySQL, Conda**  
  `source ~/.bashrc`

**2. Create Database**  
   connect to your MySQL database as the root MySQL user with the following command:  
      `$ sudo mysql`  
  
   To create a database in MySQL:  
      `create database rain_database;`  
      
   Create an account, set a password, and grant access to the database you created:  
      `create user 'rain_data'@'%' identified by '123456';`  
      `grant all on rain_database.* to 'rain_data'@'%';`  
      `FLUSH PRIVILEGES;`
      
**3. Load environment**
   ```
   conda env create -f environment.yml
   #conda activate rain_aus_env  
   #pip install django  
   #sudo apt install libmysqlclient-dev default-libmysqlclient-dev  
   #pip install mysqlclient  
   python manage.py makemigrations  
   python manage.py migrate  
   ```

**4. Run project**  
   `python manage.py crontab add`
   `python manage.py runserver your-server-ip:8000 --insecure`

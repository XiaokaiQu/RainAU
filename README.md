# RainAU

** Cloud Deployment **
The current-version project has been deployed to AWS. 
http://hiwaperth.com/

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

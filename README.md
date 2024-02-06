# RainAU

1. Install MySQL, Conda
2. Create Database
   connect to your MySQL database as the root MySQL user with the following command:
   $ sudo mysql
   To create a database in MySQL:
   create database rain_database;
   create this account, set a password, and grant access to the database you created:
   create user 'rain_data'@'%' identified by '123456';
   grant all on rain_database.* to 'rain_data'@'%';
   FLUSH PRIVILEGES;
3. Load environment
   conda activate rain_aus_env
   pip install django
   sudo apt install libmysqlclient-dev default-libmysqlclient-dev
   pip install mysqlclient
   python manage.py makemigrations
   python manage.py migrate

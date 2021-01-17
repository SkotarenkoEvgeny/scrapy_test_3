# scrapy_test_3

This scrapy project can grapthe information from **https://www.tesco.com/groceries** site.
The project uses python 3, scrapy framework, SQLalchemy library and saves to the MySQL database.

For the install a packages you can use the commands: **pip install requirements.txt** or **pipenv install --dev**.
After this successful installation, you must set information for the database connection in **.env** file (fill **.env.example** file and save him as **.env**).

For the running scrapper use a **scrapy crawl tesco** command.

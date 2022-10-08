# job_analyze


For starting the service just run 

```
python3 main.py 

```
The service requests a (https://superjob.ru) and (https://hh.ru) websites using their API and show two tables with current vacancies. Before running you have to add superjob.ru token to .env:

```
'SUPERJOBTOKEN'='YOUR TOKEN'
```

You can get the token here (https://api.superjob.ru)


Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).

# <center> Cryptocurrency Wallet <p> Python 3.10.9, Django 4.2.1, DRF 3.14.0 </center>


## Application

This application enables you to:
- create an address for a cryptocurrency 
- get previously created address located under a specified ID 
- get list of all previously created addresses


## Supported Cryptocurrencies

| Cryptocurrency    | Symbol |
| :---------------- | :----- |
| Bitcoin           | BTC    |
| Ethereum          | ETH    |
| Dogecoin          | DOGE   |
| Litecoin          | LTC    |
| Omni              | OMNI   |
| Dash              | DASH   |
| Qtum              | QTUM   |


## Local Setup

- Download and install **Python 3.10.9** <p> https://www.python.org/downloads/release/python-3109/
  
- Download and install the **venv** module  <p> https://docs.python.org/3.10/library/venv.html
<dir>
         
- Download the repository via **HTTPS**, **GitHub CLI** or with **ZIP** file<p>
*Example:* *`git clone https://github.com/danielwardega141196/crypto_wallet.git`*
<kbd>
  <img src="https://github.com/danielwardega141196/crypto_wallet/assets/28275518/0cc45026-3d3a-4808-ad77-1be0261cc83f">
</kbd>
<p>
</dir>
<br/>
         
- Open terminal and go to the repository's directory<p>
 *Example: `$ cd crypto_wallet/`*
<br/>

- Create a virtual environment for **Python 3.10**<p>
 *Example: `crypto_wallet$ virtualenv -p /usr/bin/python3.10 .venv`*
<br/>

- Activate previously created virtual environment<p>
 *Example: `crypto_wallet$ source .venv/bin/activate`*
<br/>
       
- Install requirements from **requirements.txt**<p>
 *Example: `crypto_wallet$ pip install -r requirements.txt`*
<br/>

- Run the application via **manage.py**<p>
 *Example: `crypto_wallet$ python manage.py runserver`*


## Available Endpoints

- Creation of a new cryptocurrency address: `POST /addresses/`<p>
It requires a key `symbol` representing one of the available cryptocurrency.<p>
*Example:* <p> *`curl --location 'http://127.0.0.1:8000/addresses/' --header 'Content-Type: application/json' --data '{ "symbol": "ETH" }'`*

- List of all previously created addresses: `GET /addresses/`<p>
 *Example:* <p> *`curl --location 'http://127.0.0.1:8000/addresses/'`*
  
  
- Previously created address located under a specified ID: `GET /addresses/<address_id>`<p>
 *Example:* <p> *`curl --location 'http://127.0.0.1:8000/addresses/c26be6d8-1be5-41e6-88e6-d5410f36ffde'`*


## Admin Panel

Admin Panel is available at the following address: `/admin/`<p>

 *Example:`http://127.0.0.1:8000/admin/`* <p>

<kbd>
  <img src="https://github.com/danielwardega141196/crypto_wallet/assets/28275518/26e914dd-7611-48cb-98c0-b4bb7d8bf4dd">
</kbd>
<br/>
<br/>
<kbd>
  <img src="https://github.com/danielwardega141196/crypto_wallet/assets/28275518/77408276-f68c-4389-bab8-b25b0d188e63">
</kbd>
<br/>
<br/>
<p align="center"><b>Login Credentials</b></p>
<div align="center">

| &emsp;&emsp;&emsp;&emsp;**Username**&emsp;&emsp;&emsp;&emsp; | &emsp;&emsp;&emsp;&emsp;**test_admin**&emsp;&emsp;&emsp;&emsp; |
|--------------------------------------------------------------|----------------------------------------------------------------|
| &emsp;&emsp;&emsp;&emsp;**Password**&emsp;&emsp;&emsp;&emsp; | &emsp;&emsp;&emsp;&emsp;**test_admin**&emsp;&emsp;&emsp;&emsp; |

</div>
<p align="center">Login credentials can be also created via <i>python manage.py createsuperuser</i></p>

## Tests

In order to run tests please go to repository's directory and activate the virtual environment (please see ***Local Setup***  section).<p>
Then run the following command: *`python manage.py test -v 2`*<p>
<kbd>
  <img src="https://github.com/danielwardega141196/crypto_wallet/assets/28275518/8ef262ca-1a64-4c4b-bb4b-c8a8fc031aaf">
</kbd>

## Backup

There is a possibility to make a backup of a given day via CLI. <p>
Data will be saved in the CSV file. <p>
In the next step we may think about pushing this CLI into a cron process and sending the file into the cloud storage. 

<br/>

In order to run the CLI please go to repository's directory and activate the virtual environment (please see ***Local Setup***  section).<p>
Then run the following command: *`python manage.py dump_currency_addresses <output_csv_path> <date>`*<p>

<br/>

 *Example: `crypto_wallet$ python manage.py dump_currency_addresses './test.csv' 2023-05-21`*

Date must be in `YYYY-MM-DD` format. It represents the creation date of the addresses.

<kbd>
  <img src="https://github.com/danielwardega141196/crypto_wallet/assets/28275518/21ea31b2-a3c9-460f-b411-faa1321b3cd9">
</kbd>


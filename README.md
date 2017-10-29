# Noble Internship Project

This project allows users to create accounts, and trade money between friends. Users having checkings and trading accounts and can send money to each other. For a trade to be allowed, the user's total account balance must be larger than 20% of the trade value. The same occurs for the person receiving the trade request as well.

### How to Run

1. create a virtual environment with python 3.5.2 

    `virtualenv -p python3 .`

2. clone the repository into the environment

3. run the command ... 

    `pip install -r requirements/common.txt`

4. activate the virtual environment

    `source bin/activate` 

5. cd into the root of the project

6. run the command ...

    `python app.py`
    

### Run with DOCKER

##### Alternatively, you can run this project using docker
##### Here's how to do it.

1. Make sure you have docker installed

2. `docker run -p 4000:80 alexn1336/noble-trading`
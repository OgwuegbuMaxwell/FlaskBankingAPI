![Screenshot (159)](https://github.com/OgwuegbuMaxwell/FlaskBankingAPI/assets/53094485/f6885c78-efc1-4875-935f-3f5e16e6f706)


### **FlaskBankingAPI**

The FlaskBankingAPI is a simple yet powerful banking API built using Flask and MongoDB. It supports operations such as registering users, adding funds, transferring funds between users, taking and paying loans, and checking user and bank balances.


### **Setup and Installation**

**Dependencies**

- Docker
- MongoDB
- Python 3.8+
- Flask
- Flask-RESTful
- bcrypt
- pymongo


### **Docker Configuration**

**MongoDB Container:**

Dockerfile (db):
`FROM mongo:latest
`

**Flask Application Container:**

Dockerfile (web):
`FROM python:3.8-slim`
`WORKDIR /usr/src/app`
`COPY requirements.txt .`
`RUN pip install --default-timeout=1200 --no-cache-dir -r requirements.txt`
`COPY . .`
`CMD ["python", "app.py"]`


### **Usage**

Start the service using Docker Compose:
`docker-compose up --build
`

**API Endpoints**

- **POST /register**: Register a new user or admin.
- **POST /add**: Add funds to a user's account.
- **POST /transfer**: Transfer funds between users.
- **POST /user-balance**: Check the balance of a user.
- **POST /bank-balance**: Check the balance of the bank (Admin only).
- **POST /take-loan**: Take a loan (adds a specified amount to the user's balance and debt).
- **POST /pay-loan**: Pay off a user's loan.
- **POST /update-bank-balance**: Update the bank's balance (Admin only).


**### Detailed Functionality**

**Register:**
- Registers a user with a username, password, and admin flag (optional).

**Add:**
- Adds an amount to the user's balance after deducting a transaction fee that goes to the bank.

**Transfer:**
- Transfers money between two users, including a transaction fee.

**UserBalance:**
- Retrieves the balance for a user.

**BankBalance:**
- Retrieves the balance of the bank (accessible only by admins).

**TakeLoan and **PayLoan:****
Manages loans for users, including updating debt and balances.


**Project Timeline**

**Date Started:** June 25, 2024
**Date Completed:** June 26, 2024


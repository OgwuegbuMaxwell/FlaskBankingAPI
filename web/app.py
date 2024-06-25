from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

from utilities import userExist, isAdmin, verifyCredentials, returnJson, cashWithUser, deptWithUser, updateAccount, updateDept, checkBalance, UPDATE_BANK_BALANCE
from config import app, api, users



# Register User

class Register(Resource):
    def post(self):
        postedData = request.get_json()  # Get data posted by the user
        
        username = postedData["username"]
        password = postedData["password"]
        is_admin = postedData.get("is_admin", 0)  # Default to 0 if not provided
        
        # Check if the username already exists in the database
        if userExist(username):
            return jsonify(returnJson(
                301, 
                "Username already exists. Please choose a different username."
            ))
        
        
        # Hash the password for storage
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        
        # Insert the new user into the database
        users.insert_one({
            "Username": username,
            "Password": hashed_password,
            "is_admin": int(is_admin),
            "Own": 0,
            "Dept": 0
        })
        
        # Return a success message
        return jsonify(returnJson(
            200, 
            "You have successfully signed up for the API"
        ))



class Add(Resource):
    def post(self):
        postedData = request.get_json()  # Get data posted by the user
        
        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]
        
        retJson, error = verifyCredentials(username, password)
        
        # Check if there's error in the user's credential
        if error:
            return jsonify(retJson)
        
        if money <= 0:
            return jsonify(returnJson(
                304,
                "The money amount entered must be > 0"
            ))
        
        # what does the user own at this moment
        cash = cashWithUser(username)
        # take $1 as transaction fee
        money -= 1
        bank_cash = cashWithUser("BANK")
        # Update bank balance with the 1$ transaction fee
        updateAccount("BANK", int(bank_cash) + 1) 
        updateAccount(username, int(cash) + int(money))
        
        return jsonify(returnJson(
            200,
            "Amount added successfully to account"
        ))
        
        
        
class Transfer(Resource):
    def post(self):
        postedData = request.get_json()  # Get data posted by the user
        
        username = postedData["username"]
        password = postedData["password"]
        to = postedData["to"]
        money = postedData["amount"]
        
        retJson, error = verifyCredentials(username, password)
        
        # Check if there's error in the user's credential
        if error:
            return jsonify(retJson)
        
        # Get user's balance to make sure it's enough for the transfer
        sender_balance = cashWithUser(username)     
           
        if sender_balance <= 0:
            return jsonify(returnJson(
                304,
                "You're out of money, please add or take a loan"
            ))
        
        # Check if the receiver exist
        if not userExist(to):
            return jsonify(returnJson(
                301,
                "Receiver username is invalid"
            ))
        
        # make sure the user has enough money for this transaction
        # the required money to succesfully make this transfer is the amout to
        # transfer plus transfer fee which is $1
        total_debit = int(money) + 1
        
    
        if  sender_balance < total_debit:
            return jsonify(returnJson(
                303,
                "You have insufficient balance to complete this transaction"
            ))
        
        
        # Get receiver's balance
        receiver_balance = cashWithUser(to)
        # Get BANK's balance
        bank_balance = cashWithUser("BANK")
        
        # Debit transaction fee plus the money user wants to transfer
        updateAccount(username, sender_balance - total_debit)
        
        
        # Add $1 to BANK balance as transaction fee
        updateAccount("BANK", bank_balance + 1)
        
        # Update the receiver's balance - transfer the money
        updateAccount(to, int(receiver_balance) + int(money))
        
        return jsonify(returnJson(
            200,
            f"${money} Transferred successfully"
        ))
        

# Check User's balance
class UserBalance(Resource):
    def post(self):
        postedData = request.get_json()  # Get data posted by the user
        
        username = postedData["username"]
        password = postedData["password"]
        
        # block user from check the main BANK account balance
        if username == "BANK":
            return jsonify(returnJson(
                304,
                "Warning! Unauthorized Request."
            ))
        
        # Check credentials
        retJson, error = verifyCredentials(username, password)
        
        if error:
            return jsonify(retJson)
        
        user_data = checkBalance(username)
        return jsonify(user_data)
        
        

# Check Bank balance
# You must be admin to perform this operation
class BankBalance(Resource):
    def post(self):
        postedData = request.get_json()  # Get data posted by the user
        
        username = postedData["username"]
        password = postedData["password"]
        
        # Check credentials
        retJson, error = verifyCredentials(username, password)
        
        if error:
            return jsonify(retJson)
        
        # Check if the user is admin
        is_admin = isAdmin(username)
        if not is_admin:
            return jsonify(returnJson(
                304,
                "Waarning! You are not authorized to perform this operation."
            ))
        
        bank_data = checkBalance("BANK")
        return jsonify(bank_data)

        
        
        
# take loan
class TakeLoan(Resource):
    def post(self):
        postedData = request.get_json()  # Get data posted by the user
        
        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]
        
        # verify credentials
        retJson, error = verifyCredentials(username, password)
        
        if error:
            return jsonify(retJson)
        
        # user balalance
        user_balance = cashWithUser(username)
        # user dept
        user_dept = deptWithUser(username)
        
        # Update user's main account balance - Take loan
        updateAccount(username, user_balance + money)
        
        # Update dept balance
        updateDept(username, user_dept + money)
        
        return jsonify(returnJson(
            200,
            "Loan added to your account"
        ))


# Pay loan - user should pay their loan
class PayLoan(Resource):
    def post(self):
        postedData = request.get_json()  # Get data posted by the user
        
        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]
        
        # verify credentials
        retJson, error = verifyCredentials(username, password)
        
        if error:
            return jsonify(retJson)
        
        # user balalance
        user_balance = cashWithUser(username)
        
        # Check if user have
        if user_balance < money:
            return jsonify(returnJson(
                303,
                "You have insufficient balance to complete this transaction."
            ))
        
        # If the user cross this line, that means the user has enough money for the transaction
        

        # initiate the transaction
        
        # user dept
        user_dept = deptWithUser(username)
        
        # Debit from main account
        updateAccount(username, user_balance - money)
        # Update dept balance
        updateDept(username, user_dept - money)
        
        return jsonify(returnJson(
            200,
            "Transaction Successful! Loan paid."
        ))
        

# This function is specifially for updating the main BANK balance
# not user's account balance
class UpdateBankBalance(Resource):
    def post(self):
        postedData = request.get_json()  # Get data
        
        username = postedData["username"]
        password = postedData["password"]
        amount = postedData["amount"]
        
        # Check credentials
        retJson, error = verifyCredentials(username, password)
        
        if error:
            return jsonify(retJson)
        
        # Check if the user is admin
        is_admin = isAdmin(username)
        if not is_admin:
            return jsonify(returnJson(
                304,
                "Waarning! You are not authorized to perform this operation."
            ))
        
        update = UPDATE_BANK_BALANCE(amount)
        
        if not update:
            return jsonify(returnJson(
                301,
                "Something went wrong."
            ))
        
        return jsonify(returnJson(
            200,
            f"${amount} added to the BANK successfully."
        ))
        
        
        
        
        
        
# Add resources   
api.add_resource(Register, '/register')        
api.add_resource(Add, '/add') 
api.add_resource(Transfer, '/transfer')
api.add_resource(UserBalance, '/user-balance') 
api.add_resource(BankBalance, '/bank-balance')
api.add_resource(TakeLoan, '/take-loan')
api.add_resource(PayLoan, '/pay-loan')
api.add_resource(UpdateBankBalance, '/update-bank-balance')
        
        
# RUN app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)    
       


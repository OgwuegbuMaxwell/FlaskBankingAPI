

from config import users
import bcrypt

# Check whether user exist
def userExist(username):
    return bool(users.find_one({"Username": username}))



# Helper function to verify the hashed password
def verifyPassword(username, password):
    if not userExist(username):  # Utilizing userExist to check if user exists
        return False  # Return False immediately if user does not exist

    user_data = users.find_one({"Username": username})  # Retrieves a single document
    hashed_password = user_data["Password"]
    # Check if the hashed password matches
    if bcrypt.hashpw(password.encode('utf8'), hashed_password) == hashed_password:
        return True
    return False


# Return Json 
def returnJson(status, msg):
    retJson = {
        "status": status,
        "msg": msg
    }
    return retJson


# Verify credentials
# retuen ErrorDictionar, True/False
def verifyCredentials(username, password):
    # Check if the user exists
    if not userExist(username):
        return returnJson(301, "Invalid Username"), True
    
    correct_password = verifyPassword(username, password)
    
    # Verify the password
    if not correct_password:
        return returnJson(302, "Incorrect Password"), True  # Password does not match
    
    # Both username exists and password matches. error dictionary is None
    return None, False  

    

# Helper function to retrieve the token count for a user
def countTokens(username):
    user_data = users.find_one({"Username": username})  # Retrieves a single document
    if user_data:
        tokens = user_data["Token"]
        return tokens
    return 0  # Default token count if user is not found



# Check if user is admin
def isAdmin(username):
    """
    Check if the specified user is an admin.
    
    Args:
    username (str): The username of the user to check.
    
    Returns:
    bool: True if the user is an admin, False otherwise.
    """
    user_data = users.find_one({"Username": username})
    if user_data and user_data.get("is_admin") == 1:
        return True
    return False



# Check how much the user own
def cashWithUser(username):
    user_data = users.find_one({"Username": username})  # Retrieves a single document
    if user_data:
        cash = user_data["Own"]
        return cash


# Get user's dept
def deptWithUser(username):
    user_data = users.find_one({"Username": username})  # Retrieves a single document
    if user_data:
        dept = user_data["Dept"]
        return dept
    


# Update how much the user own
def updateAccount(username, balance):
    users.update_one(
        {"Username": username},
        {"$set": {"Own": balance}}
    )


# Update user's dept
def updateDept(username, balance):
    users.update_one(
        {"Username": username},
        {"$set": {"Dept": balance}}
    )



# Check balance 
def checkBalance(username):
    user_data = users.find_one({"Username": username}, {"Password": 0, "_id": 0, "is_admin": 0})  # Excludes Password, is_admin and _id from the result
    return user_data

# Update the balance of the BANK itself
def UPDATE_BANK_BALANCE(amount):
    try:
        bank = users.find_one({"Username": "BANK"})  # Retrieves BANK
        # Retrive bank balance
        balance = bank["Own"]
        users.update_one(
            {"Username": "BANK"},
            {"$set": {"Own": int(balance) + int(amount) }}
        )
        
        return True
    except Exception as e:
        print(f"Error updating bank balance: {e}")
        return False 
        
        

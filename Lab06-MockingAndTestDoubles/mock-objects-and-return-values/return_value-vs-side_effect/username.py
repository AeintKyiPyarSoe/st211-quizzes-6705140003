class UserService:  
    def __init__(self, database):        
        self.database = database  
          
    def get_username(self, user_id):        
        return self.database.find_user(user_id)
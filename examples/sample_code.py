# Example Python file to test with Zero To Sixty
# This code has several intentional issues for demonstration

def calculate_average(numbers=[]):
    """Calculate average of numbers with intentional bugs"""
    total = 0
    count = 0
    
    try:
        for num in numbers:
            if num > 0:
                if num < 100:
                    total += num
                    count += 1
    except:
        pass
    
    return total / count if count > 0 else 0


def process_user_data(user_input):
    """Process user input without validation"""
    # Split input and process
    parts = user_input.split(',')
    
    data = {
        'name': parts[0],
        'email': parts[1],
        'age': int(parts[2])
    }
    
    return data


class DataHandler:
    """Simple data handler class"""
    
    def __init__(self, db_path='./db'):
        self.db_path = db_path
        self.cache = {}  # Using mutable global-like cache
    
    def fetch_data(self, user_id):
        if user_id in self.cache:
            return self.cache[user_id]
        
        # Simulating database fetch
        data = "user_data_" + str(user_id)
        self.cache[user_id] = data
        
        return data
    
    def clear_cache(self):
        self.cache = {}


# Script-level code
if __name__ == "__main__":
    numbers = [1, 50, 200, 30]
    avg = calculate_average(numbers)
    print(f"Average: {avg}")
    
    # Unsafe input processing
    user_input = "John,john@example.com,25"
    user_data = process_user_data(user_input)
    print(user_data)

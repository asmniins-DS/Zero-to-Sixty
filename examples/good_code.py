# Good example - Well-written Python code

from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


def calculate_average(numbers: List[float]) -> float:
    """
    Calculate the average of a list of numbers.
    
    Args:
        numbers: List of numeric values
        
    Returns:
        The average value, or 0 if list is empty
        
    Raises:
        ValueError: If any number is not numeric
    """
    if not numbers:
        return 0.0
    
    try:
        total = sum(numbers)
        return total / len(numbers)
    except TypeError as e:
        logger.error(f"Invalid input type: {e}")
        raise ValueError("All values must be numeric") from e


def process_user_data(user_input: str) -> Optional[Dict[str, Any]]:
    """
    Parse CSV-formatted user data with validation.
    
    Args:
        user_input: Comma-separated user data (name,email,age)
        
    Returns:
        Dictionary with validated user data
        
    Raises:
        ValueError: If input format is invalid
    """
    if not user_input or not user_input.strip():
        raise ValueError("Input cannot be empty")
    
    parts = user_input.split(',')
    
    if len(parts) != 3:
        raise ValueError("Expected 3 fields (name, email, age)")
    
    name, email, age_str = [p.strip() for p in parts]
    
    # Validation
    if not name:
        raise ValueError("Name cannot be empty")
    
    if '@' not in email:
        raise ValueError("Invalid email format")
    
    try:
        age = int(age_str)
        if age < 0 or age > 150:
            raise ValueError("Age must be between 0 and 150")
    except ValueError as e:
        raise ValueError(f"Invalid age: {age_str}") from e
    
    return {
        'name': name,
        'email': email,
        'age': age
    }


class DataHandler:
    """
    Manages data caching and retrieval.
    
    Attributes:
        db_path: Path to database file
        cache: In-memory cache for frequently accessed data
    """
    
    def __init__(self, db_path: str = './db') -> None:
        """Initialize handler with database path."""
        self.db_path = db_path
        self._cache: Dict[int, Any] = {}  # Use private cache
    
    def fetch_data(self, user_id: int) -> Optional[str]:
        """
        Fetch user data from cache or database.
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            User data or None if not found
        """
        if user_id in self._cache:
            logger.debug(f"Cache hit for user {user_id}")
            return self._cache[user_id]
        
        try:
            # Simulating database fetch
            data = f"user_data_{user_id}"
            self._cache[user_id] = data
            return data
        except Exception as e:
            logger.error(f"Failed to fetch data for user {user_id}: {e}")
            return None
    
    def clear_cache(self) -> None:
        """Clear all cached data."""
        self._cache.clear()
        logger.info("Cache cleared")


def main() -> None:
    """Main entry point."""
    try:
        # Test calculation
        numbers = [1, 50, 30]
        avg = calculate_average(numbers)
        print(f"Average: {avg}")
        
        # Test data processing
        user_input = "John Doe,john@example.com,25"
        user_data = process_user_data(user_input)
        print(f"User data: {user_data}")
        
        # Test data handler
        handler = DataHandler()
        data = handler.fetch_data(1)
        print(f"User data: {data}")
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()

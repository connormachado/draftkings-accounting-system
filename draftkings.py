import requests

# Base URL for the DraftKings API
BASE_URL = "https://api.draftkings.com"

# Example endpoint for fetching transaction data
TRANSACTIONS_ENDPOINT = "/transactions"

# Replace with your API key or authentication token
API_KEY = "your_api_key_here"

# Set up headers for API request
headers = {
    "Authorization": f"Bearer {API_KEY}",  # Use your token here
    "Content-Type": "application/json"
}

# Function to fetch transaction data
def get_transactions(user_id, transaction_type=None):
    """
    Fetch transaction data from DraftKings API.

    :param user_id: Your DraftKings user ID.
    :param transaction_type: (Optional) Filter for transaction type (e.g., 'sale', 'deposit').
    :return: JSON response containing transaction data.
    """
    params = {
        "userId": user_id
    }
    if transaction_type:
        params["transactionType"] = transaction_type
    
    try:
        response = requests.get(
            BASE_URL + TRANSACTIONS_ENDPOINT,
            headers=headers,
            params=params
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching transactions: {e}")
        return None

# Example usage
if __name__ == "__main__":
    user_id = "your_user_id_here"  # Replace with your DraftKings user ID
    transaction_type = "sale"  # Optional filter, e.g., "sale", "deposit"
    
    transactions = get_transactions(user_id, transaction_type)
    if transactions:
        for transaction in transactions:
            print(transaction)

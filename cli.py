import argparse     # for reading command line arguments
import requests     # to send HTTP requests to our FastAPI app
import os           # to check if token file exists

# ----------------------------
# LOAD TOKEN FUNCTION - helps the CLI "remember" the user
# ----------------------------
TOKEN_FILE = "token.txt" # File to store the JWT token

def load_token() -> str:
    #Loads the saved JWT token from token.txt (if it exists).
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            token = file.read().strip()
            print("Loaded token from token.txt")
            return token
    else:
        print("No token found. Please login first using: python cli.py login")
        return None


# ----------------------------
# HELPER FUNCTIONS (save/load token)
# ----------------------------
TOKEN_FILE = "token.txt"   # the file where token will be stored

def save_token(token: str):
    """Save token to a local file."""
    with open(TOKEN_FILE, "w") as file:
        file.write(token)
    print("Token saved to token.txt")


def load_token() -> str:
    """Read token from file if it exists."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            token = file.read().strip()
            print("Loaded saved token from token.txt")
            return token
    else:
        print("No saved token found. Please login first.")
        return None
    

# ----------------------------
# BASE URL (backend server)
# ----------------------------
BASE_URL = "http://127.0.0.1:8003"   # the port where FastAPI server is running


# ----------------------------
# SIGNUP FUNCTION
# ----------------------------
def signup(username: str, password: str):
    """
    Registers a new user on the Todo API.
    """
    # API endpoint for signup
    url = f"{BASE_URL}/auth/signup"

    # data we want to send
    payload = {
        "username": username,
        "password": password
    }

    # make a POST request to the signup endpoint
    response = requests.post(url, json=payload)
    print(f"Sending signup request to: {url}")
    print("Payload:", payload)


    # check server response
    if response.status_code == 200:
        print("Signup successful!")
        print("Response from server:", response.json())   # show token or message
    else:
        print(f"Signup failed ({response.status_code})")
        print("Details:", response.text)


# ----------------------------
# LOGIN FUNCTION
# ----------------------------
def login(username: str, password: str):
    """
    Logs in an existing user and gets JWT access token.
    """
    # API endpoint for login
    url = f"{BASE_URL}/auth/token"

    # form data required by FastAPI's OAuth2PasswordRequestForm
    payload = {
        "username": username,
        "password": password
    }

    # send POST request
    print(f"Sending login request to: {url}")
    print("Payload:", payload)
    response = requests.post(url, data=payload)

    # check server response
    if response.status_code == 200:
        data = response.json()

        #get token from the response
        token = data.get("access_token")

        print("Login successful!")
        print("Access token:", data.get("access_token"))
        print("Token type:", data.get("token_type"))

        # SAVE TOKEN TO FILE
        try:
            with open("token.txt", "w") as file:
                file.write(token)
            print("Token saved to token.txt")
        except Exception as e:
            print("Could not save token:", e)
    
    else:
        print(f"Login failed ({response.status_code})")
        print("Details:", response.text)


# ----------------------------
# ADD TODO FUNCTION
# ----------------------------
def add_todo(title: str, description: str):
    # load the saved token first
    token = load_token()
    if not token:
        return  # will stop here if user is not logged in

    # API endpoint for adding todos
    url = f"{BASE_URL}/todos/"

    # todo data we want to send
    payload = {
        "title": title,
        "description": description
    }

    # attach token for authorization
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # send POST request to backend
    print(f"Sending request to: {url}")
    print("Payload:", payload)
    response = requests.post(url, json=payload, headers=headers)

    # check response
    if response.status_code == 200:
        print("Todo created successfully!")
        print("Response:", response.json())
    else:
        print(f"Failed to create todo ({response.status_code})")
        print("Details:", response.text)


# ----------------------------
# LIST TODOS FUNCTION
# ----------------------------
# This function fetches all todos for the currently logged-in user.
# It uses the saved token from token.txt for authentication.
def list_todos():
    # load saved token
    token = load_token()
    if not token:
        return  # stop if not logged in

    # API endpoint for fetching todos
    url = f"{BASE_URL}/todos/"

    # attach authorization header
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # send GET request to backend
    print(f"Sending request to: {url}")
    response = requests.get(url, headers=headers)

    # check response
    if response.status_code == 200:
        todos = response.json()
        print("Todos fetched successfully!")
        print("------------------------------------")
        if not todos:
            print("You have no todos yet.")
        else:
            for todo in todos:
                print(f"ID: {todo['id']}")
                print(f"Title: {todo['title']}")
                print(f"Description: {todo.get('description', 'No description')}")
                print(f"Completed: {todo['completed']}")
                print(f"Created at: {todo['created_at']}")
                print("------------------------------------")
    else:
        print(f"Failed to fetch todos ({response.status_code})")
        print("Details:", response.text)


# ----------------------------
# UPDATE TODO FUNCTION
# ----------------------------
# This function updates an existing todo's title, description, or completed status.
def update_todo(todo_id: int, title: str = None, description: str = None, completed: bool = None):
    # load saved token
    token = load_token()
    if not token:
        return  # stop if not logged in

    # API endpoint for updating a todo
    url = f"{BASE_URL}/todos/{todo_id}"

    # data to update (only include fields provided by user)
    payload = {}
    if title:
        payload["title"] = title
    if description:
        payload["description"] = description
    if completed is not None:
        payload["completed"] = completed

    if not payload:
        print("No fields provided to update.")
        return

    # attach authorization header
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # send PUT request
    print(f"Sending update request to: {url}")
    print("Payload:", payload)
    response = requests.put(url, json=payload, headers=headers)

    # check response
    if response.status_code == 200:
        print("Todo updated successfully!")
        print("Response:", response.json())
    else:
        print(f"Failed to update todo ({response.status_code})")
        print("Details:", response.text)


# ----------------------------
# DELETE TODO FUNCTION
# ----------------------------
# This function deletes a todo by ID.
def delete_todo(todo_id: int):
    # load saved token
    token = load_token()
    if not token:
        return  # stop if not logged in

    # API endpoint for deleting a todo
    url = f"{BASE_URL}/todos/{todo_id}"

    # attach authorization header
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # send DELETE request
    print(f"Sending delete request to: {url}")
    response = requests.delete(url, headers=headers)

    # check response
    if response.status_code == 200:
        print("Todo deleted successfully!")
        print("Response:", response.json())
    else:
        print(f"Failed to delete todo ({response.status_code})")
        print("Details:", response.text)


# ----------------------------
# LOGOUT FUNCTION
# ----------------------------
# This function logs out the user by deleting the saved token file.
def logout():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        print("Logged out successfully. Token file deleted.")
    else:
        print("No token file found. You are already logged out.")


# ----------------------------
# WHOAMI FUNCTION
# ----------------------------
# This function shows which user is currently logged in using the saved JWT token.
def whoami():
    # load the saved token
    token = load_token()
    if not token:
        return  # stop if not logged in

    # API endpoint for checking current user
    url = f"{BASE_URL}/auth/whoami"

    # attach authorization header
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # send GET request
    print(f"Sending request to: {url}")
    response = requests.get(url, headers=headers)

    # check response
    if response.status_code == 200:
        user = response.json()
        print("Current logged-in user:")
        print(f"Username: {user['username']}")
        print(f"Created at: {user['created_at']}")
    else:
        print(f"Failed to fetch user info ({response.status_code})")
        print("Details:", response.text)


# ----------------------------
# MAIN CLI SETUP
# ----------------------------
def main():
    # Create argument parser for CLI commands
    parser = argparse.ArgumentParser(description="Todo API CLI Tool")

    # create sub-commands (like signup, login, etc.)
    subparsers = parser.add_subparsers(dest="command")

    # --- signup command ---
    signup_parser = subparsers.add_parser("signup", help="Register a new user")
    signup_parser.add_argument("--username", required=True, help="Username for new account")
    signup_parser.add_argument("--password", required=True, help="Password for new account")

    # --- login command ---
    login_parser = subparsers.add_parser("login", help="Login and get access token")
    login_parser.add_argument("--username", required=True, help="Username for existing account")
    login_parser.add_argument("--password", required=True, help="Password for existing account")

    # --- add-todo command ---
    # This command allows the logged-in user to create a new todo.
    # It sends title and description to the backend using the saved token.
    add_parser = subparsers.add_parser("add-todo", help="Create a new todo")
    add_parser.add_argument("--title", required=True, help="Title of the todo")
    add_parser.add_argument("--description", required=False, default="", help="Optional description for the todo")

    # --- list-todos command ---
    # This command shows all todos for the current logged-in user.
    list_parser = subparsers.add_parser("list-todos", help="List all todos for the logged-in user")

    # --- update-todo command ---
    # This command allows updating an existing todo's title, description, or completion status.
    update_parser = subparsers.add_parser("update-todo", help="Update an existing todo")
    update_parser.add_argument("--id", required=True, type=int, help="ID of the todo to update")
    update_parser.add_argument("--title", required=False, help="New title for the todo")
    update_parser.add_argument("--description", required=False, help="New description for the todo")
    update_parser.add_argument("--completed", required=False, type=bool, help="Mark todo as completed (True/False)")

    # --- delete-todo command ---
    # This command deletes a todo permanently using its ID.
    delete_parser = subparsers.add_parser("delete-todo", help="Delete an existing todo by ID")
    delete_parser.add_argument("--id", required=True, type=int, help="ID of the todo to delete")

    # --- logout command ---
    # This command logs out the current user by deleting the saved token file.
    subparsers.add_parser("logout", help="Logout the current user and remove saved token")

    # --- whoami command ---
    # This command shows details of the currently logged-in user using their saved token.
    subparsers.add_parser("whoami", help="Show details of the current logged-in user")

    # parse the entered command
    args = parser.parse_args()

    # run the function based on the command entered
    if args.command == "signup":
        signup(args.username, args.password)
    elif args.command == "login":
        login(args.username, args.password)
    elif args.command == "add-todo":
        add_todo(args.title, args.description)
    elif args.command == "list-todos":
        list_todos()
    elif args.command == "update-todo":
        update_todo(args.id, args.title, args.description, args.completed)
    elif args.command == "delete-todo":
        delete_todo(args.id)
    elif args.command == "logout":
        logout()
    elif args.command == "whoami":
        whoami()
    else:
        parser.print_help()


# ----------------------------
# PROGRAM ENTRY POINT
# ----------------------------
if __name__ == "__main__":
    main()

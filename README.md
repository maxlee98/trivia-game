# trivia-game
1. Install VS Code, Python 3.10.10, Postgresql (17.0), Docker
    Add the postgres to PATH if it has not been added by default (need to add the command line tools)
2. Set up the folder structure to have the main folders
    1. game-service
    2. user-service
3. Having installed Postgresql
    1. Create a new database called `trivia_game`
    2. Create a new user profile that can access to `trivia_game`, log down the login details as you need it to access via the Flask API.
4. Create the FlaskAPI Code for `user-service`
    1. Post request for the registration
    2. Post request for login
    3. Expose via port 5001
5. Create the FlaskAPI Code for `game-service`
    1. Post request for the registration
    2. Post request for login
    3. Expose via port 5002
6. Setting up of Docker and starting of services via `docker-compose.yml`




## Starting of services
1. Ensure that Docker and Postgresql (pgAdmin) is up 
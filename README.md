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


## Adding Prometheus and Grafana
1. When adding prometheus to grafana, if same docker container, the source link should be "http://prometheus:9090"

6. Automate Deployment with CI/CD
Setting up a Continuous Integration/Continuous Deployment (CI/CD) pipeline is critical for automatically building, testing, and deploying your application. Here's what you can do:

Use GitHub Actions, GitLab CI, or Jenkins to automate:
Running tests when you push code.
Building Docker images.
Deploying your updated images to a production server or cloud service.
Example for GitHub Actions to build and deploy Docker containers:

7. Scaling Your Services
- In production, you may need to scale your services based on demand. Docker Compose has limited support for scaling, so you may want to move to an orchestration platform like Kubernetes or use Docker Swarm to handle scalability.

8. Security Best Practices
Use .env files to manage environment variables, such as database passwords, API keys, etc.
Ensure secrets (e.g., passwords) are not hard-coded in your source code or Docker Compose file.
Use SSL/TLS certificates if you're deploying publicly.
Regularly update your dependencies and Docker images to avoid security vulnerabilities.

9. Document Your API
Consider adding automatic API documentation using tools like Swagger or Flask-RESTPlus. This makes it easy to share how the API works with other developers or teams.

10. Move to Cloud Hosting
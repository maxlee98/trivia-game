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

### Stop services only
docker-compose stop

### Stop and remove containers, networks..
docker-compose down 

### Down and remove volumes
docker-compose down --volumes 

### Down and remove images
docker-compose down --rmi <all|local> 


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
- Installing `kind` Kubernetes in docker
- First install `scoop` for windows or `choco` (Chocolatey)
- Install `kube` via `scoop install kubectl`
- Install `kind` via `scoop`

- Alterative would be to convert docker-compose file into Kubernetes yaml files via `kompose`
- After install kompose, convert the docker-compose.yml file into the manifests.
- First ensure that you have a cluster set up (thats why `kind` was installed)
- apply the manifest file via `kubectl apply -f <directory>`
- You can verify your deployment via `kubectl get deployments`, `kubectl get services`, `kubectl get pods`. 
- Accessing your application would be via `kubectl get services`.

8. Security Best Practices
Use .env files to manage environment variables, such as database passwords, API keys, etc.
Ensure secrets (e.g., passwords) are not hard-coded in your source code or Docker Compose file.
Use SSL/TLS certificates if you're deploying publicly.
Regularly update your dependencies and Docker images to avoid security vulnerabilities.

9. Document Your API
Consider adding automatic API documentation using tools like Swagger or Flask-RESTPlus. This makes it easy to share how the API works with other developers or teams.

10. Move to Cloud Hosting

# Learning Kubenetes with Minikube
1. Install Minikube .exe installer.
`minikube start` to start the container in docker 

https://minikube.sigs.k8s.io/docs/tutorials/kubernetes_101/module1/
Since we are running in windows instead of unix, these are the following changes:
*`set` is for windows, `export` is for unix
Following lines need to be ran in powershell instead of terminal !
Instead of `export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')`
use `$POD_NAME = kubectl get pods -o jsonpath="{.items[0].metadata.name}"` then `Write-Output $POD_NAME`

`kubectl proxy` When kubectl proxy is Useful
Accessing the Kubernetes API from the Local Machine: kubectl proxy is mainly used to forward the Kubernetes API server locally, allowing secure access to Kubernetes resources without setting up complex networking or authentication.

https://minikube.sigs.k8s.io/docs/tutorials/kubernetes_101/module3/
you may access the pod's container via `kubectl exec -ti $POD_NAME -- bash`
following which you may use `localhost` reference.

Under Module 4:
For powershell
`$NODE_PORT = kubectl get services/kubernetes-bootcamp -o jsonpath="{.spec.ports[0].nodePort}"`
`Write-Output "NODE_PORT=$NODE_PORT"`

If unable to connect after exposing port externally
`minikube addons enable ingress`
Obtain the URL for direct access to the service bypassing the variable assignment
`minikube service kubernetes-bootcamp --url`
It should provide a url. Finally you may perform something similar to such `curl http://127.0.0.1:60950`

Instead of 
> $POD_NAME = kubectl get pods -o go-template --template "{{range .items}}{{.metadata.name}}`n{{end}}"
use `$POD_NAME = kubectl get pods -o jsonpath="{.items[*].metadata.name}"`

> To remove all services and pods (starting from blank slate) `kubectl delete all --all --all-namespaces`

# Installing Helm
`choco install kubernetes-helm`
https://medium.com/@mustafaguc/how-to-easily-deploy-apache-kafka-on-kubernetes-or-locally-3375cc9d2015
`helm install kafka oci://registry-1.docker.io/bitnamicharts/kafka`

## Working from Docker-compose to deploying services
First you need to have `kompose` installed, then navigate to the folder containing the docker-compose.yml file and run `kompose convert`

Following which ensure that the host is running via `minikube start` or something.

Then apply the yaml files created from `kompose convert` after you navigate to the folder containing all the manifest files (ideally create another kubernetes file to store everything there)



# Amazon AWS Services
## Adding S3
### Creating a bucket for storage
#### Connecting to the S3 bucket via amazon cli
- You need to create an access key first to access your s3 bucket. 
    - Ideally it would be under an IAM account for security measures.
- Download the CLI and use `aws configure` to key in your credentials.


# Running of image streaming services with Docker (For now)
1. `cd .\backend\api\kafka`
2. `docker compose up` to run the docker compose file related to kafka and also start the postgres database
3. Navigate to the image-producing service and the image-consuming service on different terminals
4. Spin up the service for consuming the kafka topic by using `python app.py`
5. Do the same for the flask service to generate the images. Once flask service is up, perform a postman post request to the route to test the service.
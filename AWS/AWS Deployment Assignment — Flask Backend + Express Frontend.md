# AWS Deployment Assignment — Flask Backend + Express Frontend

**Name:** Ankur Singh
**Objective:** Deploy the To-Do app across three AWS configurations — single EC2, separate EC2 instances, and ECS/ECR/VPC containers.

> Paste your screenshots from this conversation into each `[SCREENSHOT: ...]` marker below.

---

## Task 1: Single EC2 Instance

### Setup
- Launched EC2 instance `todo-single-ec2` (Amazon Linux 2023, t2.micro, free tier)
- Security group: SSH (22), Custom TCP 3000, Custom TCP 5000, all open to required sources
- Connected via SSH using a generated key pair

`[SCREENSHOT: EC2 instance running, 2/2 status checks]`

### Deployment
- Installed Node.js, Python3, Git on the instance
- Cloned the project repo via HTTPS
- Ran Flask backend (`python app.py`, port 5000) and Express frontend (`node server.js`, port 3000) directly on the same instance, frontend configured with `BACKEND_URL=http://localhost:5000`

`[SCREENSHOT: backend and frontend logs showing both running]`

### Result

App reachable at `http://<public-ip>:3000`, form submission successfully forwarded to Flask and confirmed.

`[SCREENSHOT: browser showing form + success page]`

**Explanation:** Both services share the same host, so they communicate over `localhost` — no network hop is needed. This is the simplest deployment but has no fault isolation: if the instance goes down, both services go down together.

---

## Task 2: Separate EC2 Instances

### Setup
- Launched two instances: `todo-backend-ec2` (port 5000 open) and `todo-frontend-ec2` (port 3000 open)
- Each in its own security group, both in the same default VPC

`[SCREENSHOT: both instances running with public IPs]`

### Deployment
- Backend instance: Flask installed and run the same way as Task 1
- Frontend instance: Express installed, but `BACKEND_URL` pointed at the **backend instance's public IP** instead of localhost, since they're now separate machines communicating over the public internet

`[SCREENSHOT: frontend.log showing "Forwarding submissions to backend at http://<backend-ip>:5000"]`

### Debugging note (include for your explanation)
Initially hit `ERR_CONNECTION_REFUSED` on both ports from the browser despite the apps running correctly (`curl localhost` worked on each instance). Systematically ruled out: security groups (correct), OS firewall (not installed on this AMI), route table (had a correct `0.0.0.0/0 → igw` route). Resolved by relaunching clean instances with security groups configured correctly from the start — likely an earlier `iptables -F` command (run while debugging a different issue) had disrupted networking rules on the original instances.

### Result

`http://<frontend-public-ip>:3000` reachable, form submission travels over the public internet to the backend instance and back.

`[SCREENSHOT: browser showing form + success page]`
`[SCREENSHOT: curl http://<backend-ip>:5000/items showing the submitted item]`

**Explanation:** This setup demonstrates real network separation — frontend and backend are independently deployable and independently scalable, but now depend on the backend's public IP being stable (a real concern; production setups would use a load balancer or private DNS instead of a raw IP).

---

## Task 3: ECR + ECS + VPC

### Architecture

*(Diagram: browser → internet gateway → VPC → two public subnets, each running an ECS Fargate service; both pull images from ECR)*

### ECR — Image Registry
- Created two private repositories: `flask-todo-backend`, `express-todo-frontend`
- Built and pushed both images from local Docker

`[SCREENSHOT: docker push output for both images]`
`[SCREENSHOT: ECR console showing both repositories with "latest" tag]`

### VPC & Networking
- Used the account's default VPC: `vpc-081a643513c143584`
- Two subnets across AZs: `subnet-0e20053b1c337f9e3`, `subnet-039f532cc4ebc9de8`
- Security group `todo-ecs-sg`: inbound 3000 and 5000 open to `0.0.0.0/0`

`[SCREENSHOT: security group inbound rules]`

### ECS Cluster & Task Definitions
- Cluster: `todo-app-cluster` (Fargate, serverless — no EC2 instances to manage)
- Task definition `flask-backend-task`: 0.5 vCPU / 1GB, container port 5000, image from ECR
- Task definition `express-frontend-task`: same sizing, container port 3000, `BACKEND_URL` environment variable pointing at the backend task's public IP

`[SCREENSHOT: both task definitions listed as Active]`

### Debugging note (include for your explanation)
Cluster creation initially failed with "Unable to assume the service linked role" — resolved by explicitly creating the `AWSServiceRoleForECS` service-linked role via `aws iam create-service-linked-role`, then retrying after IAM propagation.

### ECS Services
- `flask-backend-service`: 1 task, public IP enabled, deployed in both subnets
- `express-frontend-service`: 1 task, public IP enabled, deployed after backend's IP was known

`[SCREENSHOT: backend task public IP + curl confirming it responds]`
`[SCREENSHOT: frontend form loaded from ECS task's public IP]`

### Result

`[SCREENSHOT: form submitted successfully, showing JSON response from Flask via ECS]`

**Explanation:** Unlike the EC2 approaches, this setup requires no manual server management — Fargate provisions and runs the containers, and ECS keeps the desired task count running. The trade-off demonstrated here: Fargate tasks don't have stable IPs by default (each restart gets a new one), which is why production ECS setups typically front services with an Application Load Balancer or AWS Service Connect rather than hardcoding a task's public IP as we did for this assignment.

---

## Cost Control

- All EC2 instances stopped after each task was verified working
- ECS services deleted and tasks confirmed stopped (`aws ecs list-tasks` returned empty) immediately after Task 3 was verified
- Billing alarm configured at account setup to catch any unexpected charges

`[SCREENSHOT: EC2 instances showing "Stopped" state]`
`[SCREENSHOT: aws ecs list-tasks output showing empty task list]`

## Deployed App URLs (for reference — instances/tasks stopped after verification)

- Task 1 (single EC2): `http://<public-ip>:3000` — *instance stopped*
- Task 2 (frontend EC2): `http://<public-ip>:3000` — *instance stopped*
- Task 3 (ECS frontend): `http://<public-ip>:3000` — *task stopped*

## GitHub Repository

`https://github.com/Ankur037/docker-flask-express-todo`

## Docker Hub / ECR Images

- ECR backend: `233082643027.dkr.ecr.eu-north-1.amazonaws.com/flask-todo-backend:latest`
- ECR frontend: `233082643027.dkr.ecr.eu-north-1.amazonaws.com/express-todo-frontend:latest`

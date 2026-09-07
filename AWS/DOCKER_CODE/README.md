# AWS Deployment Assignment — Resubmission

**Author:** Ankur Singh

## Deliverables (per mentor feedback)

- **GitHub repository:** https://github.com/Ankur037/docker-flask-express-todo
- **Source code:** see `/source-code` — Express frontend, Flask backend, both Dockerfiles, and `docker-compose.yml`
- **Documentation:** see `/documentation/AWS_Assignment_Documentation.docx` — full write-up of all three deployment tasks (single EC2, separate EC2, ECR/ECS/VPC) with screenshots and explanations, including the debugging process for Task 2's networking issue and the full ECR/ECS/VPC evidence chain for Task 3.
- **Deployed application:** all EC2 instances and ECS services were stopped/deleted after verification to avoid ongoing AWS charges (per the assignment's own cost-control instructions). All three were confirmed working live during development — see the documentation for verification evidence. Happy to restart any of the three for live grading on request.

## What changed since the rejected submission

1. GitHub link now included above.
2. Full source code included in this package (previously only screenshots were submitted).
3. Task 3 now has complete evidence: ECR repositories, VPC security group, ECS cluster, both task definitions, both running services, and an end-to-end verified request.
4. Task 2's troubleshooting process is documented step by step, not just the end result.

## Folder structure

```
/
├── README.md                                  (this file)
├── source-code/
│   ├── backend/        (Flask app, Dockerfile, requirements.txt)
│   ├── frontend/        (Express app, Dockerfile, package.json, public/index.html)
│   └── docker-compose.yml
└── documentation/
    └── AWS_Assignment_Documentation.docx
```

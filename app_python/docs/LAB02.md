# LAB02 — Docker Containerization

## 1. Docker Best Practices Applied

### Non-root User
The container runs the application using a non-root user created during the build process.

**Why this matters:**  
Running containers as root is a security risk. If an attacker exploits the application, they could gain root access inside the container. Using a non-root user limits potential damage and follows Docker security best practices.

**Dockerfile snippet:**
```dockerfile
RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

USER appuser
```

### Specific Base Image Version
A specific Python base image version was used: `python:3.13-slim`.

**Why this matters:**
Pinning the base image version ensures reproducible builds. Using the slim variant significantly reduces image size compared to the full image while still providing required functionality.

### Proper Layer Ordering
Dependencies are installed before copying the application source code.

**Why this matters:**  
Docker caches layers. If application code changes but dependencies do not, Docker can reuse the cached dependency layer, making rebuilds faster.

**Dockerfile snippet:**
```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
```

### Minimal File Copy
Only required runtime files are copied into the image.

**Why this matters:**
Reducing the number of files copied into the image decreases build context size, improves build speed, and reduces the final image size.

### `.dockerignore`
A `.dockerignore` file is used to exclude unnecessary files from the Docker build context.

**Why this matters:**
Docker sends the entire build context to the daemon. Excluding files such as virtual environments, Git metadata, and IDE settings improves build performance and avoids leaking development artifacts into the image.

## 2. Image Information & Decisions

### Base Image Choice
Image: python:3.13-slim
Reason:
- Smaller size compared to full Python image
- Officially maintained
- Compatible with the application requirements

### Image Size
The final image size is relatively small compared to full Python images and is suitable for production use.
This size is acceptable given that it includes:
- Python runtime
- Application dependencies
- Application source code

### Layer Structure Overview
1. Base Python image
2. Environment variable configuration
3. Non-root user creation
4. Dependency installation
5. Application code copy
6. Runtime configuration and execution
This structure balances readability, caching efficiency, and security.

## 3. Build & Run Process

### Build Image
```bash
docker build -t devops-info-service:lab02 .
```
The build completes successfully without errors.
The full build process is shown in the terminal output screenshot:
`docs/screenshots/04-docker-build.png`.

### Run Container
```bash
docker run -p 5000:5000 devops-info-service:lab02
```
The application starts correctly and listens on port `5000`.
The container startup and logs are shown in:
`docs/screenshots/05-docker-run.png`.

### Test Endpoints
Health check:
```bash
curl http://127.0.0.1:5000/health
```
Terminal output is shown in:
`docs/screenshots/06-container-health.png`.
Main endpoint:
```bash
curl -s http://127.0.0.1:5000/ | python -m json.tool
```
Formatted JSON output from the container is shown in:
`docs/screenshots/07a-container-main-endpoint.png`, `docs/screenshots/07b-container-main-endpoint.png`.
Both endpoints return valid JSON responses identical to the local (non-containerized) execution.

### Docker Hub
The image was tagged and pushed to Docker Hub using the following format:
```bash
kvassoedik/devops-info-service:lab02
```
Docker Hub repository URL:
```bash
https://hub.docker.com/r/kvassoedik/devops-info-service
```
The image is publicly accessible and can be pulled and run successfully.
The terminal output of the push & pull operations is shown in:
`docs/screenshots/08-dockerhub.png`.

## 4. Technical Analysis
### Why This Dockerfile Works
The Dockerfile follows Docker best practices by:
- Using a minimal base image
- Installing dependencies in a cached layer
- Running the application as a non-root user
- Copying only required files

### Effect of Changing Layer Order
If application code were copied before installing dependencies, Docker would reinstall dependencies on every code change, significantly slowing down rebuilds.

### Security Considerations
- Non-root execution limits container privileges
- Reduced image size lowers the attack surface
- No unnecessary tools or files are included in the runtime image

### `.dockerignore` Impact
Using `.dockerignore` reduces build context size, speeds up builds, and prevents accidental inclusion of sensitive or irrelevant files.

## 5. Challenges & Solutions

### Challenge
Understanding how Docker layer caching works and how file copy order affects rebuild performance.

### Solution
By separating dependency installation from application code copying, rebuild times were optimized while keeping the Dockerfile readable and maintainable.

## 6. Summary

In this lab, the application from Lab 1 was successfully containerized using Docker.
The resulting image follows security and performance best practices, runs identically to the local application, and is published to Docker Hub for reuse and deployment.

This containerized setup provides a solid foundation for future labs involving CI/CD pipelines, monitoring, and Kubernetes deployment.
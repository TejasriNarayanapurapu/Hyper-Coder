import os
import subprocess

def generate_dockerfile(project_path: str):
    """
    Creates a simple Dockerfile in the given project directory.
    """
    dockerfile_content = """
    FROM python:3.10-slim

    WORKDIR /app

    COPY . /app

    RUN pip install --no-cache-dir -r requirements.txt

    CMD ["python", "app/main.py"]
    """

    dockerfile_path = os.path.join(project_path, "Dockerfile")
    with open(dockerfile_path, "w") as f:
        f.write(dockerfile_content.strip())

    return f"Dockerfile created at {dockerfile_path}"

def build_docker_image(project_path: str, image_name: str):
    """
    Builds a Docker image from the Dockerfile in project_path.
    """
    command = ["docker", "build", "-t", image_name, project_path]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        return f"Docker image '{image_name}' built successfully."
    else:
        return f"Error building Docker image:\n{result.stderr}"

def run_docker_container(image_name: str, port: int = 8501):
    """
    Runs the Docker container exposing the given port.
    """
    command = [
        "docker", "run", "-p", f"{port}:{port}", image_name
    ]
    try:
        subprocess.run(command)
        return f"Docker container running on port {port}."
    except Exception as e:
        return f"Error running Docker container: {e}"

if __name__ == "__main__":
    project_dir = "/path/to/your/HyperCoder"
    image = "hypercoder-image"

    print(generate_dockerfile(project_dir))
    print(build_docker_image(project_dir, image))
    # Uncomment below to run container (blocking call)
    # print(run_docker_container(image, port=8501))


# AI Pilot

**AI Pilot** is a project that integrates a FastAPI application with the **Ollama** service to generate text using large language models (LLMs). It leverages GPU-accelerated performance for optimal efficiency and includes a fully Dockerized environment for easy deployment and scalability.

---

## Why This Is Awesome 🚀

- **GPU Acceleration**: Uses NVIDIA GPUs to speed up inference for large language models.
- **FastAPI**: A modern, high-performance Python API framework.
- **Modular Architecture**: Separated services for clean integration and scalability.
- **Dockerized**: Seamless setup with Docker Compose.
- **Customizable**: Plug-and-play support for Ollama models like Llama2 and Mistral.
- **Persistent Storage**: Data is persisted using Docker volumes.

---

## Prerequisites ✅

### For Windows Users

1. **NVIDIA GPU**: Ensure you have a compatible NVIDIA GPU with **compute capability 5.0 or higher**.  
   Check compatibility here: [NVIDIA CUDA GPUs](https://developer.nvidia.com/cuda-gpus).

2. **Install NVIDIA Drivers**:  
   Download and install the latest drivers for your GPU from [NVIDIA's Drivers Page](https://www.nvidia.com/Download/index.aspx).

3. **Install WSL 2**:  
   Docker on Windows requires WSL 2 for GPU acceleration. Follow these steps to install and configure WSL 2:

   **Enable WSL and Install Ubuntu:**:
   Open PowerShell as Administrator and execute:
	
   ```powershell
   wsl --install -d Ubuntu
   ```
   This command installs WSL with the default Ubuntu distribution.
   
   **Set WSL 2 as Default Version**:  
   After installation, reboot your system and install Ubuntu (or a preferred Linux distro) from the Microsoft Store.
	
   ```powershell
   wsl --set-default-version 2
   ```
	
   For detailed instructions, refer to [Microsoft's documentation] (https://learn.microsoft.com/en-us/windows/ai/directml/gpu-cuda-in-wsl?utm_source=chatgpt.com). 

4. **Install Docker Desktop**:  
   Download Docker Desktop for Windows from [Docker's Website](https://www.docker.com/products/docker-desktop/). Enable **WSL 2 integration** during installation.

5. **Install NVIDIA Container Toolkit for WSL**:  

   Run the following commands inside your WSL terminal (Ubuntu):

   **Set Up the Package Repository**:

   ```bash
   sudo 
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
   curl -s -L https://nvidia.github.io/libnvidia-container/stable/$distribution/nvidia-container-toolkit.list | \
   sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
   sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
   sudo apt-get update
   ```

   **Install the Toolkit**:

   ```bash
   sudo apt-get install -y nvidia-container-toolkit
   ```

   **Configure Docker to Use NVIDIA Runtime**:

   ```bash
   sudo nvidia-ctk runtime configure --runtime=docker
   sudo systemctl restart docker
   ```

   For detailed instructions, refer to the [NVIDIA WSL2 Guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html).

---

## Step-by-Step Setup 🛠️

### **1. Pull the Ollama Docker Image**

Pull the latest Ollama Docker image optimized for GPU usage:

```bash
docker pull ollama/ollama:latest
```

---

### **2. Run the Ollama Docker Container**

Start the Ollama container with GPU support:

```bash
docker run -d --gpus all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama:latest
```

**Flags Explanation**:
- `--gpus all`: Grants the container access to all available GPUs.
- `-v ollama:/root/.ollama`: Mounts a Docker volume named `ollama` to persist data.
- `-p 11434:11434`: Maps the Ollama API port.
- `--name ollama`: Names the container "ollama".

---

### **3. Verify GPU Utilization**

To confirm that the container is using your GPU:

**Check Running Containers**:

```bash
docker ps
```

**Access the Container**:

```bash
docker exec -it ollama /bin/bash
```

**Check GPU Status**:

```bash
nvidia-smi
```

You should see your GPU status, confirming it is accessible.

---

### **4. Run a Model with Ollama**

**Pull a Model** (e.g., Llama 2):

```bash
docker exec -it ollama ollama pull llama2
```

**Run the Model**:

```bash
docker exec -it ollama ollama run llama2
```

---

### **5. Build and Start the Project**

Run the following command to build and start the services using Docker Compose:

```bash
docker-compose up -d --build
```

This will start:
- **Ollama Service**: Runs the specified model.
- **FastAPI Service**: A RESTful API to interact with Ollama.

---

### **6. Interact with the API**

Send a POST request to generate text:

```bash
curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d '{"prompt": "Once upon a time"}'
```

**Response Example**:

```json
{
  "response": "Once upon a time, in a land far, far away..."
}
```

---

### **7. Stop the Services**

To stop all running services:

```bash
docker-compose down
```

---

## FastAPI Endpoints

| Method | Endpoint      | Description             |
|--------|---------------|-------------------------|
| POST   | `/generate`   | Generate text from a model prompt. |

**Request Example**:

```json
{
  "prompt": "Tell me a story about AI"
}
```

---

## Notes

1. Ensure NVIDIA drivers and the NVIDIA Container Toolkit are installed correctly.
2. Verify your GPU compatibility with `nvidia-smi` before running.
3. Models like Llama 2 can take time to load; be patient during the initial run.
4. Modify `docker-compose.yml` to include additional models or configurations.

---

## Why Use This Project?

- **Easy Setup**: Pre-configured Docker Compose makes deployment simple.
- **Scalability**: Add more containers or models as needed.
- **Performance**: GPU-accelerated inference ensures optimal speed.
- **Extensibility**: Use FastAPI to expose new endpoints and functionalities.

---

## Credits

- **FastAPI**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **Ollama**: [https://ollama.com/](https://ollama.com/)
- **NVIDIA Docker Toolkit**: [https://developer.nvidia.com/nvidia-docker](https://developer.nvidia.com/nvidia-docker)

---

### Explanation of `docker-compose.yml`

The `docker-compose.yml` file defines two main services: **Ollama** and **FastAPI**.

#### Ollama Service
- **Purpose**: Runs the Ollama service with GPU support and specified models.
- **Configuration**:
   - `--gpus all`: Grants access to all GPUs on the host machine.
   - `-v ollama:/root/.ollama`: Persists Ollama model data in a Docker volume.
   - `-p 11434:11434`: Exposes port `11434` for API communication.
- **Model Management**: Models like **Llama2** are pulled and served from this container.

#### FastAPI Service
- **Purpose**: Provides a RESTful API to interact with the Ollama service.
- **Configuration**:
   - Exposes port `8000` for accessing the FastAPI endpoints.
   - Depends on the Ollama service for text generation.

---

### Running Docker Compose

To start both services (**Ollama** and **FastAPI**) simultaneously, use the following command:

```bash
docker-compose up -d --build
```

- **`up`**: Starts all services defined in `docker-compose.yml`.
- **`-d`**: Runs the services in **detached mode** (in the background).
- **`--build`**: Rebuilds the images if there are changes to the `Dockerfile`.

---

### Verify Running Services

To check that both services are running:

```bash
docker-compose ps
```

You should see both `ollama` and `fastapi` services listed as **running**.

---

### Why Use `docker-compose`?

- **Simplicity**: Launches multiple services with a single command.
- **Networking**: Automatically creates a shared network for services to communicate.
- **Scalability**: Easily add more containers or services in the future.

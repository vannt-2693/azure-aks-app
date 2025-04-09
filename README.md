# Azure image app

## Build on local

- build
```bash
docker build -t azure-image-app .
```

- run
```bash
docker run -p 5001:5000 \
       -e AZURE_STORAGE_CONNECTION_STRING="YOUR_AZURE_STORAGE_CONNECTION_STRING" \
       -e AZURE_STORAGE_CONTAINER_NAME="your-container-name" \
       --name my-azure-app \
       azure-image-app
```

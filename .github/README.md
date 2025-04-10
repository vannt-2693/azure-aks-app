# Workflow for CICD

- Create service principal for cicd
```bash
az ad sp create-for-rbac --name $project-$env-iac --role="Contributor" --scopes="/subscriptions/68ed087f-4be0-41e8-a682-b1bce367af23/resourceGroups/project-dev-rg/providers/Microsoft.ContainerService/managedClusters/project-dev-aks-api-cluster"

# The command should output a JSON object similar to this:
{
  "clientId": "<GUID>",
  "clientSecret": "<STRING>",
  "subscriptionId": "<GUID>",
  "tenantId": "<GUID>",
  "resourceManagerEndpointUrl": "<URL>"
  (...)
}
```

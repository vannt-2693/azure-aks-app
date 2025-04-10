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

{
  "appId": "ae529a19-8399-48c9-bb75-b0a0f72591f9",
  "displayName": "project-dev-aks-sp",
  "password": "mVW8Q~gSRY3PTEmcRC50tbGXrVm1N.Ka~QZRVcmZ",
  "tenant": "ea78b286-8e8d-4e16-8e78-96f3870c32b9"
}

{
    "clientSecret": "mVW8Q~gSRY3PTEmcRC50tbGXrVm1N.Ka~QZRVcmZ",
    "subscriptionId": "68ed087f-4be0-41e8-a682-b1bce367af23",
    "tenantId":  "ea78b286-8e8d-4e16-8e78-96f3870c32b9",
    "clientId":  "ae529a19-8399-48c9-bb75-b0a0f72591f9"
}

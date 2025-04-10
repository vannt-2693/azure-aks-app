{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "aks-app-chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "aks-app-chart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "aks-app-chart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "aks-app-chart.labels" -}}
helm.sh/chart: {{ include "aks-app-chart.chart" . }}
{{ include "aks-app-chart.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "aks-app-chart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "aks-app-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "aks-app-chart.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "aks-app-chart.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Helper to get the SecretStore name
*/}}
{{- define "aks-app-chart.secretStoreName" -}}
{{- printf "%s%s" (include "aks-app-chart.fullname" .) .Values.externalSecrets.secretStore.nameSuffix }}
{{- end -}}

{{/*
Helper to get the ExternalSecret name (which is also the target K8s secret name by default in the template)
*/}}
{{- define "aks-app-chart.externalSecretName" -}}
{{- printf "%s%s" (include "aks-app-chart.fullname" .) .Values.externalSecrets.externalSecret.nameSuffix }}
{{- end -}}

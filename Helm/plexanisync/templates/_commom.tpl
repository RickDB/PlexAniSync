{{/*
Not using enough of the bitnami common library chart, to warrant a full chart dependency
https://github.dev/bitnami/charts/blob/main/bitnami/common
*/}}

{{/*
Expand the name of the chart.
*/}}
{{- define "common.names.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "common.names.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "common.names.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Allow the release namespace to be overridden for multi-namespace deployments in combined charts.
*/}}
{{- define "common.names.namespace" -}}
{{- default .Release.Namespace .Values.namespaceOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Kubernetes standard labels
{{ include "common.labels.standard" (dict "customLabels" .Values.commonLabels "context" $) -}}
*/}}
{{- define "common.labels.standard" -}}
app.kubernetes.io/name: {{ include "common.names.name" . | quote }}
helm.sh/chart: {{ include "common.names.chart" . | quote }}
app.kubernetes.io/instance: {{ .Release.Name | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service | quote }}
{{- end -}}

{{/*
Labels used on immutable fields such as deploy.spec.selector.matchLabels or svc.spec.selector
*/}}
{{- define "common.labels.matchLabels" -}}
app.kubernetes.io/name: {{ include "common.names.name" . | quote }}
app.kubernetes.io/instance: {{ .Release.Name | quote }}
{{- end -}}

{{- define "pod.volumes" -}}
{{- if or .Values.custom_mappings .Values.volumes }}
volumes:
  {{- if .Values.custom_mappings }}
  - configMap:
      defaultMode: 0777
      name: {{ include "common.names.fullname" . }}
    name: {{ include "common.names.fullname" . }}
  {{- end }}
  {{- if .Values.volumes }}
    {{- toYaml .Values.volumes | nindent 2 }}
  {{- end }}
{{- end }}
{{- end }}

{{- define "container.volumeMounts" -}}
{{- if or .Values.custom_mappings .Values.volumeMounts }}
volumeMounts:
  {{- if .Values.custom_mappings }}
  - mountPath: /plexanisync/custom_mappings.yaml
    name: {{ include "common.names.fullname" . }}
    subPath: custom_mappings.yaml
  {{- end }}
  {{- if .Values.volumeMounts }}
    {{- toYaml .Values.volumeMounts | nindent 2 -}}
  {{- end }}
{{- end }}
{{- end }}

{{- define "container.env" -}}
- name: PLEX_SECTION
  value: {{ .Values.settings.plex_section | quote }}
- name: PLEX_URL
  value: {{ .Values.settings.plex_url | required ".Values.settings.plex_url is required" | quote }}
- name: ANI_USERNAME
  value: {{ .Values.settings.ani_username | required ".Values.settings.ani_username is required" | quote }}
- name: PLEX_TOKEN
  valueFrom:
    secretKeyRef:
      key: plex-token
      name: {{ include "common.names.fullname" . }}
- name: ANI_TOKEN
  valueFrom:
    secretKeyRef:
      key: ani-token
      name: {{ include "common.names.fullname" . }}
{{- if .Values.settings.plex_episode_count_priority }}
- name: PLEX_EPISODE_COUNT_PRIORITY
  value: {{ .Values.settings.plex_episode_count_priority | quote }}
{{- end }}
{{- if .Values.settings.sync_ratings }}
- name: SYNC_RATINGS
  value: {{ .Values.settings.sync_ratings | quote }}
{{- end }}
{{- if .Values.settings.skip_list_update }}
- name: SKIP_LIST_UPDATE
  value: {{ .Values.settings.skip_list_update | quote }}
{{- end }}
{{- with .Values.envVars }}
  {{- toYaml . | nindent 8 }}
{{- end }}
{{- end }}

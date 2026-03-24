/**
 * Environment configuration for the Agent Assist UI.
 *
 * All client-side config is read from Vite environment variables
 * (prefixed with VITE_) per the zero-hardcoding policy.
 */
export const config = {
  /** URL of the UI Connector WebSocket/REST service. */
  uiConnectorUrl: import.meta.env.VITE_UI_CONNECTOR_URL || 'http://localhost:8080',

  /** Dialogflow API location (e.g. 'global', 'us-central1'). */
  dialogflowLocation: import.meta.env.VITE_DIALOGFLOW_LOCATION || 'global',
} as const

export type AppConfig = typeof config

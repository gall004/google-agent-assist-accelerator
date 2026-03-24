/**
 * Environment configuration for the Agent Assist Sidecar (simulator).
 *
 * All client-side config is read from Vite environment variables.
 */
export const config = {
  /** URL of the UI Connector WebSocket/REST service. */
  uiConnectorUrl:
    import.meta.env.VITE_UI_CONNECTOR_URL || 'http://localhost:8080',

  /** Dialogflow API location. */
  dialogflowLocation: import.meta.env.VITE_DIALOGFLOW_LOCATION || 'global',

  /** Port for the sidecar dev server. */
  port: parseInt(import.meta.env.VITE_PORT || '5174'),

  /** Allowed origin for the ui iframe (for postMessage validation). */
  uiOrigin: import.meta.env.VITE_UI_ORIGIN || 'http://localhost:5173',

  /** URL to embed in the iframe. */
  uiEmbedUrl: import.meta.env.VITE_UI_EMBED_URL || 'http://localhost:5173',
} as const

export type AppConfig = typeof config

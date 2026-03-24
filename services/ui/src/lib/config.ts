/**
 * Environment configuration for the Agent Assist UI.
 *
 * All client-side config is read from Vite environment variables
 * (prefixed with VITE_) per the zero-hardcoding policy.
 */
export const config = {
  /** URL of the UI Connector WebSocket/REST service. */
  uiConnectorUrl:
    import.meta.env.VITE_UI_CONNECTOR_URL || 'http://localhost:8080',

  /** Dialogflow API location (e.g. 'global', 'us-central1'). */
  dialogflowLocation: import.meta.env.VITE_DIALOGFLOW_LOCATION || 'global',

  /** Allowed parent origin for postMessage (the sidecar/CRM host). */
  parentOrigin:
    import.meta.env.VITE_PARENT_ORIGIN || 'http://localhost:5174',

  /** Dialogflow conversation profile resource name. */
  conversationProfileName:
    import.meta.env.VITE_CONVERSATION_PROFILE || '',

  /** Communication channel: 'voice' or 'chat'. */
  channel: (import.meta.env.VITE_CHANNEL || 'voice') as 'voice' | 'chat',

  /** Custom API endpoint (proxy) for Dialogflow calls. */
  apiEndpoint: import.meta.env.VITE_API_ENDPOINT || '',

  /** Auth token for Dialogflow API (dev only). */
  authToken: import.meta.env.VITE_AUTH_TOKEN || '',

  /** Agent Assist features to render (comma-separated). */
  features:
    import.meta.env.VITE_AA_FEATURES ||
    'CONVERSATION_SUMMARIZATION,SMART_REPLY,KNOWLEDGE_SEARCH',
} as const

export type AppConfig = typeof config

/**
 * TypeScript declarations for Google Agent Assist UI Module globals.
 *
 * These are injected via script tags in index.html:
 * - https://www.gstatic.com/agent-assist-ui-modules/v1/common.js
 * - https://www.gstatic.com/agent-assist-ui-modules/v2/container.js
 */

/** Configuration for the event-based connector (WebSocket). */
interface EventBasedConfig {
  transport?: 'websocket' | 'polling'
  library?: 'SocketIo'
  notifierServerEndpoint: string
}

/** API configuration for the connector. */
interface ApiConfig {
  authToken: string
  customApiEndpoint?: string
  apiKey?: string
  headers?: Array<{ key: string; value: string }>
}

/** Full connector configuration. */
interface ConnectorConfig {
  channel: 'chat' | 'voice'
  agentDesktop:
    | 'LivePerson'
    | 'GenesysCloud'
    | 'SalesForce'
    | 'GenesysEngageWwe'
    | 'Custom'
  conversationProfileName: string
  apiConfig: ApiConfig
  eventBasedConfig?: EventBasedConfig
  uiModuleEventOptions?: { namespace: string }
}

/** Global UiModulesConnector class exposed by common.js. */
declare class UiModulesConnector {
  constructor()
  init(config: ConnectorConfig): void
  disconnect(): void
  setAuthToken(token: string): void
}

/**
 * Dispatch an event to the Google Agent Assist UI module system.
 *
 * @param eventName - The event name (e.g. 'active-conversation-selected').
 * @param options - Event options with a detail payload.
 */
declare function dispatchAgentAssistEvent(
  eventName: string,
  options: { detail: unknown },
): void

/**
 * Subscribe to events from the Google Agent Assist UI module system.
 *
 * @param eventName - The event name to listen for.
 * @param handler - Callback receiving the event.
 */
declare function addAgentAssistEventListener(
  eventName: string,
  handler: (event: { detail: unknown }) => void,
): void

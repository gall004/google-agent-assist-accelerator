import { useEffect, useRef, useCallback } from 'react'
import { config } from '../lib/config'
import type { ActiveCall } from '../types/cti'

/**
 * Event bridge between our CTI system and Google Agent Assist UI Modules.
 *
 * Initializes the UiModulesConnector (from common.js) and provides methods
 * to dispatch native Google events when our CTI state changes.
 *
 * Uses imperative DOM APIs — React synthetic events don't work reliably
 * with custom web components.
 */
export function useAgentAssistConnector() {
  const connectorRef = useRef<UiModulesConnector | null>(null)
  const initializedRef = useRef(false)

  useEffect(() => {
    if (initializedRef.current) return
    if (typeof UiModulesConnector === 'undefined') return

    try {
      const connector = new UiModulesConnector()
      connector.init({
        channel: config.channel,
        agentDesktop: 'Custom',
        conversationProfileName: config.conversationProfileName,
        apiConfig: {
          authToken: config.authToken,
          customApiEndpoint: config.apiEndpoint || undefined,
        },
        eventBasedConfig: {
          transport: 'websocket',
          library: 'SocketIo',
          notifierServerEndpoint: config.uiConnectorUrl,
        },
      })

      connectorRef.current = connector
      initializedRef.current = true
    } catch {
      // Google scripts not loaded yet — expected in test/dev
    }

    return () => {
      connectorRef.current?.disconnect()
      connectorRef.current = null
      initializedRef.current = false
    }
  }, [])

  /**
   * Dispatch active-conversation-selected to load the Google modules
   * for a specific conversation.
   */
  const selectConversation = useCallback((call: ActiveCall) => {
    if (typeof dispatchAgentAssistEvent === 'undefined') return

    dispatchAgentAssistEvent('active-conversation-selected', {
      detail: {
        conversationId: call.conversationId,
        conversationProfileName: config.conversationProfileName,
      },
    })
  }, [])

  /** Update the connector auth token at runtime. */
  const updateAuthToken = useCallback((token: string) => {
    connectorRef.current?.setAuthToken(token)
  }, [])

  return { selectConversation, updateAuthToken }
}

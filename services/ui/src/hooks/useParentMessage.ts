import { useCallback } from 'react'
import { config } from '../lib/config'
import type { ActiveCall, ParentMessage } from '../types/cti'

/**
 * Sends origin-validated postMessage to the parent window (sidecar/CRM).
 *
 * Used when the agent clicks the Soft Pop notification to instruct the
 * parent CRM to navigate to the customer record.
 *
 * @returns sendNavigateToRecord callback.
 */
export function useParentMessage() {
  const sendNavigateToRecord = useCallback((call: ActiveCall) => {
    if (!window.parent || window.parent === window) return

    const message: ParentMessage = {
      type: 'NAVIGATE_TO_RECORD',
      payload: {
        conversationId: call.conversationId,
        callerName: call.callerName,
        phoneNumber: call.phoneNumber,
        intent: call.intent,
      },
    }

    window.parent.postMessage(message, config.parentOrigin)
  }, [])

  return { sendNavigateToRecord }
}

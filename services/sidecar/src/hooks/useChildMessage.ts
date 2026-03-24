import { useEffect, useCallback, useState } from 'react'
import { config } from '../lib/config'
import type { NavigateToRecordMessage, CustomerRecord } from '../types/cti'

/**
 * Listens for postMessage from the ui iframe with strict origin validation.
 *
 * On NAVIGATE_TO_RECORD: updates the mock CRM to show the customer record.
 * Messages from unknown origins are dropped (logged in dev).
 *
 * @returns The current customer record and a clear function.
 */
export function useChildMessage() {
  const [record, setRecord] = useState<CustomerRecord | null>(null)

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.origin !== config.uiOrigin) return

      const data = event.data as NavigateToRecordMessage
      if (data?.type === 'NAVIGATE_TO_RECORD') {
        setRecord({
          conversationId: data.payload.conversationId,
          callerName: data.payload.callerName,
          phoneNumber: data.payload.phoneNumber,
          intent: data.payload.intent,
        })
      }
    }

    window.addEventListener('message', handleMessage)
    return () => window.removeEventListener('message', handleMessage)
  }, [])

  const clearRecord = useCallback(() => setRecord(null), [])

  return { record, clearRecord }
}

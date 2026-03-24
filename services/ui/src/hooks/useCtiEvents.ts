import { useEffect, useState, useCallback } from 'react'
import type { Socket } from 'socket.io-client'
import type { CtiEvent, ActiveCall } from '../types/cti'

/**
 * Listens for CTI events on the WebSocket and manages active call state.
 *
 * @param socket - The socket.io Socket instance (from useSocket).
 * @returns Active call state, showSoftPop flag, and a dismiss handler.
 */
export function useCtiEvents(socket: Socket | null) {
  const [activeCall, setActiveCall] = useState<ActiveCall | null>(null)
  const [showSoftPop, setShowSoftPop] = useState(false)

  const dismissSoftPop = useCallback(() => setShowSoftPop(false), [])

  useEffect(() => {
    if (!socket) return

    const handleCtiEvent = (event: CtiEvent) => {
      switch (event.event_type) {
        case 'call_started':
          setActiveCall({
            conversationId: event.conversation_id,
            callerName: event.caller_data.caller_name,
            phoneNumber: event.caller_data.phone_number,
            intent: event.caller_data.intent,
            status: 'ringing',
            startTime: event.timestamp,
          })
          setShowSoftPop(true)
          break

        case 'agent_answered':
          setActiveCall((prev) =>
            prev?.conversationId === event.conversation_id
              ? { ...prev, status: 'connected' }
              : prev,
          )
          setShowSoftPop(false)
          break

        case 'call_ended':
          setActiveCall((prev) =>
            prev?.conversationId === event.conversation_id
              ? { ...prev, status: 'ended' }
              : prev,
          )
          setShowSoftPop(false)
          break
      }
    }

    socket.on('cti_event', handleCtiEvent)
    return () => {
      socket.off('cti_event', handleCtiEvent)
    }
  }, [socket])

  const clearCall = useCallback(() => setActiveCall(null), [])

  return { activeCall, showSoftPop, dismissSoftPop, clearCall }
}

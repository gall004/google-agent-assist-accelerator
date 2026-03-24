import { useEffect, useRef, useState, useCallback } from 'react'
import { io, Socket } from 'socket.io-client'
import { config } from '../lib/config'
import type { CtiEvent } from '../types/cti'

/** Mock CTI event payloads per the project appendix. */
const MOCK_EVENTS: Record<string, CtiEvent> = {
  call_started: {
    event_type: 'call_started',
    conversation_id: 'conv-aaa-12345',
    timestamp: new Date().toISOString(),
    caller_data: {
      phone_number: '+15550198372',
      caller_name: 'John Doe',
      intent: 'Claims Inquiry',
    },
  },
  agent_answered: {
    event_type: 'agent_answered',
    conversation_id: 'conv-aaa-12345',
    timestamp: new Date().toISOString(),
    agent_id: 'agent-77',
  },
  call_ended: {
    event_type: 'call_ended',
    conversation_id: 'conv-aaa-12345',
    timestamp: new Date().toISOString(),
    reason: 'customer_disconnected',
  },
}

/**
 * CTI Developer Panel for dispatching mock backend events.
 *
 * Connects directly to the ui-connector via socket.io and emits
 * cti_event payloads, mirroring how a real CTI adapter would inject
 * events into the system.
 */
export function CtiPanel() {
  const socketRef = useRef<Socket | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [lastEvent, setLastEvent] = useState<string | null>(null)

  useEffect(() => {
    const socket = io(config.uiConnectorUrl, {
      transports: ['websocket', 'polling'],
    })

    socket.on('connect', () => setIsConnected(true))
    socket.on('disconnect', () => setIsConnected(false))

    socketRef.current = socket

    return () => {
      socket.disconnect()
      socketRef.current = null
    }
  }, [])

  const dispatchEvent = useCallback((eventType: string) => {
    const socket = socketRef.current
    if (!socket?.connected) return

    const event = {
      ...MOCK_EVENTS[eventType],
      timestamp: new Date().toISOString(),
    }

    socket.emit('cti_event', event)
    setLastEvent(eventType)
  }, [])

  return (
    <div className="cti-panel" data-testid="cti-panel">
      <div className="cti-panel__header">
        <h3>CTI Developer Panel</h3>
        <span
          className={`cti-panel__status ${isConnected ? 'cti-panel__status--on' : ''}`}
        >
          {isConnected ? '● Connected' : '○ Disconnected'}
        </span>
      </div>

      <div className="cti-panel__buttons">
        <button
          onClick={() => dispatchEvent('call_started')}
          className="cti-btn cti-btn--start"
          data-testid="cti-start-call"
        >
          📞 Start Call
        </button>
        <button
          onClick={() => dispatchEvent('agent_answered')}
          className="cti-btn cti-btn--answer"
          data-testid="cti-answer-call"
        >
          ✅ Answer Call
        </button>
        <button
          onClick={() => dispatchEvent('call_ended')}
          className="cti-btn cti-btn--end"
          data-testid="cti-end-call"
        >
          ⏹ End Call
        </button>
      </div>

      {lastEvent && (
        <div className="cti-panel__log" data-testid="cti-last-event">
          Last dispatched: <code>{lastEvent}</code>
        </div>
      )}
    </div>
  )
}

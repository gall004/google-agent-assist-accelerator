import type { ActiveCall } from '../types/cti'

interface ActiveCallBarProps {
  /** Current active call, or null if idle. */
  call: ActiveCall | null
  /** Whether the WebSocket is connected. */
  isConnected: boolean
}

/**
 * Status bar showing the active call information or idle state.
 *
 * Displays caller name, intent, conversation ID, and call status.
 */
export function ActiveCallBar({ call, isConnected }: ActiveCallBarProps) {
  return (
    <div className="active-call-bar" data-testid="active-call-bar">
      <div className="active-call-bar__status">
        <span
          className={`status-dot ${isConnected ? 'status-dot--connected' : 'status-dot--disconnected'}`}
        />
        {isConnected ? 'Connected' : 'Disconnected'}
      </div>

      {call && call.status !== 'idle' ? (
        <div className="active-call-bar__info">
          <span className="active-call-bar__caller">{call.callerName}</span>
          <span className="active-call-bar__intent">{call.intent}</span>
          <span
            className={`active-call-bar__call-status active-call-bar__call-status--${call.status}`}
          >
            {call.status.toUpperCase()}
          </span>
        </div>
      ) : (
        <div className="active-call-bar__info">
          <span className="active-call-bar__idle">No active call</span>
        </div>
      )}
    </div>
  )
}

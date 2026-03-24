import { useEffect, useCallback } from 'react'
import type { ActiveCall } from '../types/cti'

/** Auto-dismiss timeout in milliseconds. */
const AUTO_DISMISS_MS = 15_000

interface SoftPopNotificationProps {
  /** The incoming call to display. */
  call: ActiveCall
  /** Whether to show the notification. */
  visible: boolean
  /** Called when the notification is dismissed. */
  onDismiss: () => void
  /** Called when the agent clicks to accept/open the record. */
  onAccept: (call: ActiveCall) => void
}

/**
 * Non-intrusive toast notification for incoming calls.
 *
 * Slides in from the top-right when a call_started event fires.
 * Clicking the notification triggers CRM navigation + Google module load.
 * Auto-dismisses after 15 seconds if not interacted with.
 */
export function SoftPopNotification({
  call,
  visible,
  onDismiss,
  onAccept,
}: SoftPopNotificationProps) {
  useEffect(() => {
    if (!visible) return
    const timer = setTimeout(onDismiss, AUTO_DISMISS_MS)
    return () => clearTimeout(timer)
  }, [visible, onDismiss])

  const handleClick = useCallback(() => {
    onAccept(call)
    onDismiss()
  }, [call, onAccept, onDismiss])

  if (!visible) return null

  return (
    <div
      className="soft-pop"
      role="alert"
      aria-live="assertive"
      onClick={handleClick}
      data-testid="soft-pop-notification"
    >
      <div className="soft-pop__icon">📞</div>
      <div className="soft-pop__content">
        <p className="soft-pop__title">Incoming Call</p>
        <p className="soft-pop__message">
          <strong>{call.callerName}</strong> — {call.intent}
        </p>
        <p className="soft-pop__cta">Click to open record</p>
      </div>
      <button
        className="soft-pop__close"
        onClick={(e) => {
          e.stopPropagation()
          onDismiss()
        }}
        aria-label="Dismiss notification"
        data-testid="soft-pop-close"
      >
        ✕
      </button>
    </div>
  )
}

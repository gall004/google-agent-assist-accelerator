import { useEffect, useRef } from 'react'
import { config } from '../lib/config'

/**
 * React wrapper for the Google <agent-assist-ui-modules-v2> web component.
 *
 * Mounts the custom element imperatively via useRef and DOM APIs.
 * React synthetic events don't reliably work with custom web components,
 * so all attribute setting and event binding uses standard DOM methods.
 */
export function AgentAssistContainer() {
  const containerRef = useRef<HTMLDivElement>(null)
  const mountedRef = useRef(false)

  useEffect(() => {
    const container = containerRef.current
    if (mountedRef.current || !container) return

    /* Only mount if the custom element is registered (scripts loaded). */
    if (!customElements.get('agent-assist-ui-modules-v2')) return

    const el = document.createElement('agent-assist-ui-modules-v2')
    el.setAttribute('features', config.features)
    el.setAttribute('hide-header', 'true')

    container.appendChild(el)
    mountedRef.current = true

    return () => {
      if (container.contains(el)) {
        container.removeChild(el)
      }
      mountedRef.current = false
    }
  }, [])

  return (
    <div
      ref={containerRef}
      className="aa-container"
      data-testid="agent-assist-container"
    />
  )
}

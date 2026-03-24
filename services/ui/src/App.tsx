import { useCallback } from 'react'
import { useSocket } from './hooks/useSocket'
import { useCtiEvents } from './hooks/useCtiEvents'
import { useAgentAssistConnector } from './hooks/useAgentAssistConnector'
import { useParentMessage } from './hooks/useParentMessage'
import { SoftPopNotification } from './components/SoftPopNotification'
import { AgentAssistContainer } from './components/AgentAssistContainer'
import { ActiveCallBar } from './components/ActiveCallBar'
import type { ActiveCall } from './types/cti'

/**
 * Root application component for the Agent Assist UI widget.
 *
 * Orchestrates the WebSocket connection, CTI event handling,
 * Google Agent Assist Container V2, and Soft Pop UX.
 */
function App() {
  const { socket, isConnected } = useSocket()
  const { activeCall, showSoftPop, dismissSoftPop } = useCtiEvents(socket)
  const { selectConversation } = useAgentAssistConnector()
  const { sendNavigateToRecord } = useParentMessage()

  const handleSoftPopAccept = useCallback(
    (call: ActiveCall) => {
      sendNavigateToRecord(call)
      selectConversation(call)
    },
    [sendNavigateToRecord, selectConversation],
  )

  return (
    <div id="agent-assist-root" className="agent-assist-app">
      <ActiveCallBar call={activeCall} isConnected={isConnected} />

      {activeCall && (
        <SoftPopNotification
          call={activeCall}
          visible={showSoftPop}
          onDismiss={dismissSoftPop}
          onAccept={handleSoftPopAccept}
        />
      )}

      <div className="agent-assist-app__container">
        <AgentAssistContainer />
      </div>
    </div>
  )
}

export default App

import { useChildMessage } from './hooks/useChildMessage'
import { DynamicsLayout } from './components/DynamicsLayout'

/**
 * Root application for the Sidecar (Microsoft Dynamics simulator).
 *
 * Listens for postMessage from the Agent Assist ui iframe and
 * renders the mock Dynamics environment with the CTI Developer Panel.
 */
function App() {
  const { record } = useChildMessage()

  return <DynamicsLayout record={record} />
}

export default App

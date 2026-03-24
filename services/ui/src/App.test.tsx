import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

/* Mock all hooks to avoid socket.io side effects in tests */
vi.mock('./hooks/useSocket', () => ({
  useSocket: () => ({ socket: null, isConnected: false }),
}))

vi.mock('./hooks/useCtiEvents', () => ({
  useCtiEvents: () => ({
    activeCall: null,
    showSoftPop: false,
    dismissSoftPop: vi.fn(),
    clearCall: vi.fn(),
  }),
}))

vi.mock('./hooks/useAgentAssistConnector', () => ({
  useAgentAssistConnector: () => ({
    selectConversation: vi.fn(),
    updateAuthToken: vi.fn(),
  }),
}))

vi.mock('./hooks/useParentMessage', () => ({
  useParentMessage: () => ({ sendNavigateToRecord: vi.fn() }),
}))

describe('App', () => {
  it('should render the root element', () => {
    render(<App />)
    expect(screen.getByTestId('active-call-bar')).toBeInTheDocument()
  })

  it('should render the Agent Assist container', () => {
    render(<App />)
    expect(screen.getByTestId('agent-assist-container')).toBeInTheDocument()
  })

  it('should show disconnected status when no socket', () => {
    render(<App />)
    expect(screen.getByText('Disconnected')).toBeInTheDocument()
  })
})

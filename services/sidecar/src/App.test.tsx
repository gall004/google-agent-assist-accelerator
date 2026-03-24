import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

/* Mock the hooks to isolate rendering */
vi.mock('./hooks/useChildMessage', () => ({
  useChildMessage: () => ({ record: null, clearRecord: vi.fn() }),
}))

/* Mock CtiPanel to avoid socket.io side effects */
vi.mock('./components/CtiPanel', () => ({
  CtiPanel: () => <div data-testid="cti-panel">CTI Mock</div>,
}))

describe('App', () => {
  it('should render the Dynamics layout', () => {
    render(<App />)
    expect(screen.getByTestId('dynamics-layout')).toBeInTheDocument()
  })

  it('should render the Agent Assist iframe', () => {
    render(<App />)
    expect(screen.getByTestId('agent-assist-iframe')).toBeInTheDocument()
  })

  it('should render the CRM record area', () => {
    render(<App />)
    expect(screen.getByTestId('crm-record')).toBeInTheDocument()
  })
})

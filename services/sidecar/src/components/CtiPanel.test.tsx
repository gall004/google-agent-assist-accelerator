import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { CtiPanel } from './CtiPanel'

/* Mock socket.io-client */
const mockOn = vi.fn()
const mockEmit = vi.fn()
const mockDisconnect = vi.fn()
const mockSocket = {
  on: mockOn,
  emit: mockEmit,
  disconnect: mockDisconnect,
  connected: true,
}

vi.mock('socket.io-client', () => ({
  io: vi.fn(() => mockSocket),
}))

describe('CtiPanel', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('should render the panel with three buttons', () => {
    render(<CtiPanel />)
    expect(screen.getByTestId('cti-panel')).toBeInTheDocument()
    expect(screen.getByTestId('cti-start-call')).toBeInTheDocument()
    expect(screen.getByTestId('cti-answer-call')).toBeInTheDocument()
    expect(screen.getByTestId('cti-end-call')).toBeInTheDocument()
  })

  it('should emit call_started event when Start Call is clicked', () => {
    render(<CtiPanel />)
    fireEvent.click(screen.getByTestId('cti-start-call'))
    expect(mockEmit).toHaveBeenCalledWith(
      'cti_event',
      expect.objectContaining({ event_type: 'call_started' }),
    )
  })

  it('should emit agent_answered event when Answer Call is clicked', () => {
    render(<CtiPanel />)
    fireEvent.click(screen.getByTestId('cti-answer-call'))
    expect(mockEmit).toHaveBeenCalledWith(
      'cti_event',
      expect.objectContaining({ event_type: 'agent_answered' }),
    )
  })

  it('should emit call_ended event when End Call is clicked', () => {
    render(<CtiPanel />)
    fireEvent.click(screen.getByTestId('cti-end-call'))
    expect(mockEmit).toHaveBeenCalledWith(
      'cti_event',
      expect.objectContaining({ event_type: 'call_ended' }),
    )
  })

  it('should display the last dispatched event', () => {
    render(<CtiPanel />)
    fireEvent.click(screen.getByTestId('cti-start-call'))
    expect(screen.getByTestId('cti-last-event')).toHaveTextContent(
      'call_started',
    )
  })
})

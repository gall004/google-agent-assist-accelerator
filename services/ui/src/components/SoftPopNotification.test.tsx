import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { SoftPopNotification } from './SoftPopNotification'
import type { ActiveCall } from '../types/cti'

describe('SoftPopNotification', () => {
  const mockCall: ActiveCall = {
    conversationId: 'conv-123',
    callerName: 'John Doe',
    phoneNumber: '+15550001234',
    intent: 'Claims Inquiry',
    status: 'ringing',
    startTime: '2026-01-01T00:00:00Z',
  }

  const mockDismiss = vi.fn()
  const mockAccept = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should render when visible', () => {
    render(
      <SoftPopNotification
        call={mockCall}
        visible={true}
        onDismiss={mockDismiss}
        onAccept={mockAccept}
      />,
    )

    expect(screen.getByTestId('soft-pop-notification')).toBeInTheDocument()
    expect(screen.getByText('John Doe')).toBeInTheDocument()
    expect(screen.getByText(/Claims Inquiry/)).toBeInTheDocument()
  })

  it('should not render when hidden', () => {
    render(
      <SoftPopNotification
        call={mockCall}
        visible={false}
        onDismiss={mockDismiss}
        onAccept={mockAccept}
      />,
    )

    expect(screen.queryByTestId('soft-pop-notification')).not.toBeInTheDocument()
  })

  it('should call onAccept and onDismiss when clicked', () => {
    render(
      <SoftPopNotification
        call={mockCall}
        visible={true}
        onDismiss={mockDismiss}
        onAccept={mockAccept}
      />,
    )

    fireEvent.click(screen.getByTestId('soft-pop-notification'))
    expect(mockAccept).toHaveBeenCalledWith(mockCall)
    expect(mockDismiss).toHaveBeenCalled()
  })

  it('should dismiss without accepting when close button clicked', () => {
    render(
      <SoftPopNotification
        call={mockCall}
        visible={true}
        onDismiss={mockDismiss}
        onAccept={mockAccept}
      />,
    )

    fireEvent.click(screen.getByTestId('soft-pop-close'))
    expect(mockDismiss).toHaveBeenCalled()
    expect(mockAccept).not.toHaveBeenCalled()
  })

  it('should auto-dismiss after timeout', () => {
    vi.useFakeTimers()

    render(
      <SoftPopNotification
        call={mockCall}
        visible={true}
        onDismiss={mockDismiss}
        onAccept={mockAccept}
      />,
    )

    vi.advanceTimersByTime(15_000)
    expect(mockDismiss).toHaveBeenCalled()

    vi.useRealTimers()
  })
})

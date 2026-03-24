import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useCtiEvents } from './useCtiEvents'
import type { CtiEvent } from '../types/cti'

describe('useCtiEvents', () => {
  const mockOn = vi.fn()
  const mockOff = vi.fn()
  const mockSocket = { on: mockOn, off: mockOff } as never

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should initialize with no active call', () => {
    const { result } = renderHook(() => useCtiEvents(null))
    expect(result.current.activeCall).toBeNull()
    expect(result.current.showSoftPop).toBe(false)
  })

  it('should subscribe to cti_event on mount', () => {
    renderHook(() => useCtiEvents(mockSocket))
    expect(mockOn).toHaveBeenCalledWith('cti_event', expect.any(Function))
  })

  it('should set activeCall on call_started', () => {
    const { result } = renderHook(() => useCtiEvents(mockSocket))
    const handler = mockOn.mock.calls.find(
      ([event]) => event === 'cti_event',
    )?.[1]

    const event: CtiEvent = {
      event_type: 'call_started',
      conversation_id: 'conv-123',
      timestamp: '2026-01-01T00:00:00Z',
      caller_data: {
        phone_number: '+15550001234',
        caller_name: 'Jane Smith',
        intent: 'Billing',
      },
    }

    act(() => handler(event))

    expect(result.current.activeCall).toEqual({
      conversationId: 'conv-123',
      callerName: 'Jane Smith',
      phoneNumber: '+15550001234',
      intent: 'Billing',
      status: 'ringing',
      startTime: '2026-01-01T00:00:00Z',
    })
    expect(result.current.showSoftPop).toBe(true)
  })

  it('should update status on agent_answered', () => {
    const { result } = renderHook(() => useCtiEvents(mockSocket))
    const handler = mockOn.mock.calls.find(
      ([event]) => event === 'cti_event',
    )?.[1]

    act(() =>
      handler({
        event_type: 'call_started',
        conversation_id: 'conv-123',
        timestamp: '2026-01-01T00:00:00Z',
        caller_data: {
          phone_number: '+1555',
          caller_name: 'Test',
          intent: 'X',
        },
      }),
    )

    act(() =>
      handler({
        event_type: 'agent_answered',
        conversation_id: 'conv-123',
        timestamp: '2026-01-01T00:00:15Z',
        agent_id: 'agent-1',
      }),
    )

    expect(result.current.activeCall?.status).toBe('connected')
    expect(result.current.showSoftPop).toBe(false)
  })

  it('should update status on call_ended', () => {
    const { result } = renderHook(() => useCtiEvents(mockSocket))
    const handler = mockOn.mock.calls.find(
      ([event]) => event === 'cti_event',
    )?.[1]

    act(() =>
      handler({
        event_type: 'call_started',
        conversation_id: 'conv-123',
        timestamp: '2026-01-01T00:00:00Z',
        caller_data: {
          phone_number: '+1555',
          caller_name: 'Test',
          intent: 'X',
        },
      }),
    )

    act(() =>
      handler({
        event_type: 'call_ended',
        conversation_id: 'conv-123',
        timestamp: '2026-01-01T00:15:00Z',
        reason: 'customer_disconnected',
      }),
    )

    expect(result.current.activeCall?.status).toBe('ended')
  })

  it('should unsubscribe on unmount', () => {
    const { unmount } = renderHook(() => useCtiEvents(mockSocket))
    unmount()
    expect(mockOff).toHaveBeenCalledWith('cti_event', expect.any(Function))
  })
})

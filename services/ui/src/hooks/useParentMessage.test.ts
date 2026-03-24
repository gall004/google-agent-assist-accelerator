import { describe, it, expect, vi, beforeEach, afterAll } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useParentMessage } from './useParentMessage'
import type { ActiveCall } from '../types/cti'

describe('useParentMessage', () => {
  const mockPostMessage = vi.fn()
  const originalParent = window.parent

  beforeEach(() => {
    vi.clearAllMocks()
    Object.defineProperty(window, 'parent', {
      value: { postMessage: mockPostMessage },
      writable: true,
      configurable: true,
    })
  })

  afterAll(() => {
    Object.defineProperty(window, 'parent', {
      value: originalParent,
      writable: true,
      configurable: true,
    })
  })

  it('should send NAVIGATE_TO_RECORD with correct payload', () => {
    const { result } = renderHook(() => useParentMessage())

    const call: ActiveCall = {
      conversationId: 'conv-123',
      callerName: 'John Doe',
      phoneNumber: '+15550001234',
      intent: 'Claims',
      status: 'ringing',
      startTime: '2026-01-01T00:00:00Z',
    }

    act(() => result.current.sendNavigateToRecord(call))

    expect(mockPostMessage).toHaveBeenCalledWith(
      {
        type: 'NAVIGATE_TO_RECORD',
        payload: {
          conversationId: 'conv-123',
          callerName: 'John Doe',
          phoneNumber: '+15550001234',
          intent: 'Claims',
        },
      },
      'http://localhost:5174',
    )
  })

  it('should use the configured parentOrigin as targetOrigin', () => {
    const { result } = renderHook(() => useParentMessage())

    const call: ActiveCall = {
      conversationId: 'c',
      callerName: 'A',
      phoneNumber: '+1',
      intent: 'B',
      status: 'ringing',
      startTime: '',
    }

    act(() => result.current.sendNavigateToRecord(call))

    /* Second argument to postMessage is the targetOrigin */
    const targetOrigin = mockPostMessage.mock.calls[0][1]
    expect(targetOrigin).not.toBe('*')
    expect(typeof targetOrigin).toBe('string')
  })
})

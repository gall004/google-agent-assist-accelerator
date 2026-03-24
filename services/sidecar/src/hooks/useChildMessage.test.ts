import { describe, it, expect, vi } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useChildMessage } from './useChildMessage'

describe('useChildMessage', () => {
  it('should initialize with no record', () => {
    const { result } = renderHook(() => useChildMessage())
    expect(result.current.record).toBeNull()
  })

  it('should update record on valid NAVIGATE_TO_RECORD message', () => {
    const { result } = renderHook(() => useChildMessage())

    act(() => {
      window.dispatchEvent(
        new MessageEvent('message', {
          origin: 'http://localhost:5173',
          data: {
            type: 'NAVIGATE_TO_RECORD',
            payload: {
              conversationId: 'conv-123',
              callerName: 'John Doe',
              phoneNumber: '+15550001234',
              intent: 'Claims',
            },
          },
        }),
      )
    })

    expect(result.current.record).toEqual({
      conversationId: 'conv-123',
      callerName: 'John Doe',
      phoneNumber: '+15550001234',
      intent: 'Claims',
    })
  })

  it('should ignore messages from unknown origins', () => {
    const { result } = renderHook(() => useChildMessage())

    act(() => {
      window.dispatchEvent(
        new MessageEvent('message', {
          origin: 'https://evil.example.com',
          data: {
            type: 'NAVIGATE_TO_RECORD',
            payload: {
              conversationId: 'x',
              callerName: 'x',
              phoneNumber: 'x',
              intent: 'x',
            },
          },
        }),
      )
    })

    expect(result.current.record).toBeNull()
  })

  it('should clear record when clearRecord is called', () => {
    const { result } = renderHook(() => useChildMessage())

    act(() => {
      window.dispatchEvent(
        new MessageEvent('message', {
          origin: 'http://localhost:5173',
          data: {
            type: 'NAVIGATE_TO_RECORD',
            payload: {
              conversationId: 'c',
              callerName: 'A',
              phoneNumber: '+1',
              intent: 'B',
            },
          },
        }),
      )
    })

    expect(result.current.record).not.toBeNull()

    act(() => result.current.clearRecord())
    expect(result.current.record).toBeNull()
  })

  it('should unsubscribe on unmount', () => {
    const spy = vi.fn()

    /* Temporarily override to track removal */
    const original = window.removeEventListener.bind(window)
    window.removeEventListener = (...args: Parameters<typeof original>) => {
      if (args[0] === 'message') spy()
      original(...args)
    }

    const { unmount } = renderHook(() => useChildMessage())
    unmount()

    expect(spy).toHaveBeenCalled()
    window.removeEventListener = original
  })
})

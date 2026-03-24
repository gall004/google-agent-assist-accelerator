import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useSocket } from './useSocket'

/* Mock socket.io-client */
const mockOn = vi.fn()
const mockConnect = vi.fn()
const mockDisconnect = vi.fn()
const mockOff = vi.fn()
const mockSocket = {
  on: mockOn,
  off: mockOff,
  connect: mockConnect,
  disconnect: mockDisconnect,
  connected: false,
}

vi.mock('socket.io-client', () => ({
  io: vi.fn(() => mockSocket),
}))

describe('useSocket', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('should initialize with disconnected state', () => {
    const { result } = renderHook(() => useSocket())
    expect(result.current.isConnected).toBe(false)
  })

  it('should return the socket instance', () => {
    const { result } = renderHook(() => useSocket())
    expect(result.current.socket).toBe(mockSocket)
  })

  it('should set isConnected to true on connect event', () => {
    const { result } = renderHook(() => useSocket())

    const connectHandler = mockOn.mock.calls.find(
      ([event]) => event === 'connect',
    )?.[1]
    expect(connectHandler).toBeDefined()

    act(() => connectHandler())
    expect(result.current.isConnected).toBe(true)
  })

  it('should set isConnected to false on disconnect event', () => {
    const { result } = renderHook(() => useSocket())

    const connectHandler = mockOn.mock.calls.find(
      ([event]) => event === 'connect',
    )?.[1]
    const disconnectHandler = mockOn.mock.calls.find(
      ([event]) => event === 'disconnect',
    )?.[1]

    act(() => connectHandler())
    expect(result.current.isConnected).toBe(true)

    act(() => disconnectHandler())
    expect(result.current.isConnected).toBe(false)
  })

  it('should disconnect on unmount', () => {
    const { unmount } = renderHook(() => useSocket())
    unmount()
    expect(mockDisconnect).toHaveBeenCalled()
  })
})

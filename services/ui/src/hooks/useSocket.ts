import { useEffect, useRef, useState, useMemo } from 'react'
import { io, Socket } from 'socket.io-client'
import { config } from '../lib/config'

/**
 * Manages socket.io-client lifecycle.
 *
 * Connects to the ui-connector on mount and disconnects on unmount.
 * Socket.io handles reconnection with exponential backoff internally.
 *
 * @returns Socket instance and connection status.
 */
export function useSocket() {
  const [isConnected, setIsConnected] = useState(false)

  const socket = useMemo(
    () =>
      io(config.uiConnectorUrl, {
        transports: ['websocket', 'polling'],
        reconnection: true,
        reconnectionAttempts: Infinity,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 10000,
        autoConnect: false,
      }),
    [],
  )

  useEffect(() => {
    socket.on('connect', () => setIsConnected(true))
    socket.on('disconnect', () => setIsConnected(false))
    socket.connect()

    return () => {
      socket.disconnect()
    }
  }, [socket])

  return { socket, isConnected }
}

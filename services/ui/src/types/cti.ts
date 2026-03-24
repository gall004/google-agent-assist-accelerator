/**
 * CTI event type definitions for Agent Assist.
 *
 * These types match the mock payloads dispatched by the sidecar CTI Panel
 * and received via WebSocket from the ui-connector.
 */

/** Caller metadata attached to a call_started event. */
export interface CallerData {
  phone_number: string
  caller_name: string
  intent: string
}

/** Dispatched when a new call is routed to the agent. */
export interface CallStartedEvent {
  event_type: 'call_started'
  conversation_id: string
  timestamp: string
  caller_data: CallerData
}

/** Dispatched when the agent picks up the call. */
export interface AgentAnsweredEvent {
  event_type: 'agent_answered'
  conversation_id: string
  timestamp: string
  agent_id: string
}

/** Dispatched when the call ends. */
export interface CallEndedEvent {
  event_type: 'call_ended'
  conversation_id: string
  timestamp: string
  reason: string
}

/** Union of all CTI event types. */
export type CtiEvent = CallStartedEvent | AgentAnsweredEvent | CallEndedEvent

/** Call status for UI state management. */
export type CallStatus = 'ringing' | 'connected' | 'ended' | 'idle'

/** Active call state tracked by the UI. */
export interface ActiveCall {
  conversationId: string
  callerName: string
  phoneNumber: string
  intent: string
  status: CallStatus
  startTime: string
}

/** PostMessage payload sent from ui to sidecar parent. */
export interface NavigateToRecordMessage {
  type: 'NAVIGATE_TO_RECORD'
  payload: {
    conversationId: string
    callerName: string
    phoneNumber: string
    intent: string
  }
}

/** Union of all postMessage message types. */
export type ParentMessage = NavigateToRecordMessage

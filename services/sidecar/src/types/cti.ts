/**
 * CTI event and postMessage type definitions for the sidecar simulator.
 *
 * Mirrors the ui service types for cross-boundary communication.
 */

/** Caller metadata. */
export interface CallerData {
  phone_number: string
  caller_name: string
  intent: string
}

/** call_started event payload. */
export interface CallStartedEvent {
  event_type: 'call_started'
  conversation_id: string
  timestamp: string
  caller_data: CallerData
}

/** agent_answered event payload. */
export interface AgentAnsweredEvent {
  event_type: 'agent_answered'
  conversation_id: string
  timestamp: string
  agent_id: string
}

/** call_ended event payload. */
export interface CallEndedEvent {
  event_type: 'call_ended'
  conversation_id: string
  timestamp: string
  reason: string
}

/** Union of all CTI event types. */
export type CtiEvent = CallStartedEvent | AgentAnsweredEvent | CallEndedEvent

/** PostMessage payload received from the ui iframe. */
export interface NavigateToRecordMessage {
  type: 'NAVIGATE_TO_RECORD'
  payload: {
    conversationId: string
    callerName: string
    phoneNumber: string
    intent: string
  }
}

/** Customer record data displayed in the mock CRM. */
export interface CustomerRecord {
  conversationId: string
  callerName: string
  phoneNumber: string
  intent: string
}

import type { CustomerRecord } from '../types/cti'

interface CustomerRecordViewProps {
  record: CustomerRecord | null
}

/**
 * Mock customer record display for the Dynamics simulator.
 *
 * Shows the customer data received via the Soft Pop → postMessage flow.
 */
export function CustomerRecordView({ record }: CustomerRecordViewProps) {
  if (!record) {
    return (
      <div className="crm-record crm-record--empty" data-testid="crm-record">
        <div className="crm-record__placeholder">
          <span className="crm-record__icon">👤</span>
          <p>No customer record selected</p>
          <p className="crm-record__hint">
            Use the CTI Panel to simulate a call, then click the Soft Pop
            notification in the Agent Assist widget.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="crm-record" data-testid="crm-record">
      <div className="crm-record__header">
        <h2>{record.callerName}</h2>
        <span className="crm-record__badge">Active</span>
      </div>
      <div className="crm-record__fields">
        <div className="crm-record__field">
          <label>Phone</label>
          <span>{record.phoneNumber}</span>
        </div>
        <div className="crm-record__field">
          <label>Intent</label>
          <span>{record.intent}</span>
        </div>
        <div className="crm-record__field">
          <label>Conversation ID</label>
          <span className="crm-record__mono">{record.conversationId}</span>
        </div>
      </div>
    </div>
  )
}

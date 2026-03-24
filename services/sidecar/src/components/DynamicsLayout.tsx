import { config } from '../lib/config'
import { CtiPanel } from './CtiPanel'
import { CustomerRecordView } from './CustomerRecordView'
import type { CustomerRecord } from '../types/cti'

interface DynamicsLayoutProps {
  /** Customer record from postMessage. */
  record: CustomerRecord | null
}

/**
 * Mock Microsoft Dynamics single-session layout.
 *
 * Simulates the Dynamics agent desktop with:
 * - Dark top navigation bar
 * - Left sidebar (navigation items)
 * - Main content area (CRM record + CTI Panel)
 * - Right sidebar (Agent Assist ui iframe)
 */
export function DynamicsLayout({ record }: DynamicsLayoutProps) {
  return (
    <div className="dynamics-layout" data-testid="dynamics-layout">
      {/* Top Nav */}
      <header className="dynamics-nav">
        <div className="dynamics-nav__brand">
          <span className="dynamics-nav__logo">◆</span>
          Dynamics 365 — Agent Desktop Simulator
        </div>
        <div className="dynamics-nav__actions">
          <span className="dynamics-nav__user">Agent Demo</span>
        </div>
      </header>

      <div className="dynamics-body">
        {/* Left Sidebar */}
        <nav className="dynamics-sidebar">
          <ul className="dynamics-sidebar__nav">
            <li className="dynamics-sidebar__item dynamics-sidebar__item--active">
              📋 Cases
            </li>
            <li className="dynamics-sidebar__item">👥 Contacts</li>
            <li className="dynamics-sidebar__item">📊 Dashboard</li>
            <li className="dynamics-sidebar__item">📁 Knowledge</li>
          </ul>
        </nav>

        {/* Main Content Area */}
        <main className="dynamics-main">
          <CustomerRecordView record={record} />
          <CtiPanel />
        </main>

        {/* Right Sidebar — Agent Assist Widget */}
        <aside className="dynamics-agent-assist">
          <div className="dynamics-agent-assist__header">Agent Assist</div>
          <iframe
            src={config.uiEmbedUrl}
            className="dynamics-agent-assist__iframe"
            title="Agent Assist Widget"
            data-testid="agent-assist-iframe"
            allow="microphone"
          />
        </aside>
      </div>
    </div>
  )
}

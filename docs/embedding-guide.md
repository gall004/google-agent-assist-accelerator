# Embedding Guide

> **Status:** Planned for Phase 3+. This document will be populated when the embed widget architecture is designed.

## Overview

The Agent Assist Accelerator UI is designed to be embedded in various CRM and CCaaS platforms. Each platform will have a dedicated embed widget under `services/embed-widgets/<platform>/`.

## Planned Integrations

| Platform | Status | Widget Location |
|---|---|---|
| Cisco Finesse | Planned | `services/embed-widgets/cisco-finesse/` |
| Genesys Cloud | Planned | `services/embed-widgets/genesys-cloud/` |
| Salesforce | Planned | `services/embed-widgets/salesforce/` |
| Microsoft Dynamics | Planned | `services/embed-widgets/dynamics/` |
| ServiceNow | Planned | `services/embed-widgets/servicenow/` |

## Architecture

Each embed widget will:
1. Load the Agent Assist UI as an iframe or web component
2. Listen for platform-specific CTI events (call start, call end, agent state changes)
3. Map platform events to the Agent Assist event model
4. Communicate with the UI Connector for real-time suggestions

import { describe, it, expect } from 'vitest'
import { config } from '../lib/config'

describe('config', () => {
  it('provides default ui connector URL', () => {
    expect(config.uiConnectorUrl).toBeTruthy()
    expect(typeof config.uiConnectorUrl).toBe('string')
  })

  it('provides default dialogflow location', () => {
    expect(config.dialogflowLocation).toBe('global')
  })
})

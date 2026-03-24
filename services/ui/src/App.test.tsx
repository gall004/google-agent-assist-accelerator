import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('renders the application root', () => {
    render(<App />)
    expect(screen.getByText('Agent Assist UI')).toBeInTheDocument()
  })

  it('has the correct root element id', () => {
    const { container } = render(<App />)
    expect(container.querySelector('#agent-assist-root')).toBeInTheDocument()
  })

  it('renders scaffold placeholder text', () => {
    render(<App />)
    expect(screen.getByText(/scaffold initialized/i)).toBeInTheDocument()
  })
})

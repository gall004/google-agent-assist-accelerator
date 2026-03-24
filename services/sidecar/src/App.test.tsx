import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('renders the sidecar root', () => {
    render(<App />)
    expect(screen.getByText('Agent Desktop Simulator')).toBeInTheDocument()
  })

  it('has the correct root element id', () => {
    const { container } = render(<App />)
    expect(container.querySelector('#sidecar-root')).toBeInTheDocument()
  })

  it('renders scaffold placeholder text', () => {
    render(<App />)
    expect(screen.getByText(/sidecar scaffold initialized/i)).toBeInTheDocument()
  })
})

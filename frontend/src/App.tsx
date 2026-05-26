import { useState } from 'react'
import Chat from './components/Chat'
import MemoryPanel from './components/MemoryPanel'
import type { Message, ChatResponse } from './types'

export default function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [memories, setMemories] = useState<string[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  async function sendMessage() {
    if (!input.trim()) return

    const userMessage = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setLoading(true)

    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage,
          session_id: 'session_1',
          user_id: 'mazen'
        })
      })

      const data: ChatResponse = await res.json()
      setMessages(prev => [...prev, { role: 'agent', content: data.response }])
      setMemories(data.memories_used)
    } catch {
      setMessages(prev => [...prev, { role: 'agent', content: 'Something went wrong. Is the backend running?' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-screen bg-zinc-950 text-zinc-100 flex flex-col">
      <header className="px-6 py-4 border-b border-zinc-800 flex items-center gap-3">
        <h1 className="text-lg font-semibold tracking-tight">MemoryOS</h1>
        <span className="text-xs text-zinc-500">persistent memory for AI agents</span>
      </header>

      <div className="flex flex-1 overflow-hidden">
        <div className="flex-1 flex flex-col border-r border-zinc-800">
          <Chat
            messages={messages}
            input={input}
            loading={loading}
            onInputChange={setInput}
            onSend={sendMessage}
          />
        </div>

        <div className="w-80 overflow-y-auto">
          <MemoryPanel memories={memories} />
        </div>
      </div>
    </div>
  )
}

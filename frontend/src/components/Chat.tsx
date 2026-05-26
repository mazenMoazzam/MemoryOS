import type { Message } from '../types'

interface Props {
  messages: Message[]
  input: string
  loading: boolean
  onInputChange: (val: string) => void
  onSend: () => void
}

export default function Chat({ messages, input, loading, onInputChange, onSend }: Props) {
  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto space-y-3 p-4">
        {messages.length === 0 && (
          <p className="text-zinc-500 text-sm text-center mt-8">
            Start a conversation. MemoryOS will remember it.
          </p>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`max-w-[80%] px-4 py-2 rounded-lg text-sm whitespace-pre-wrap ${
              msg.role === 'user'
                ? 'ml-auto bg-blue-600 text-white'
                : 'bg-zinc-800 text-zinc-100'
            }`}
          >
            {msg.content}
          </div>
        ))}
        {loading && (
          <div className="bg-zinc-800 text-zinc-400 px-4 py-2 rounded-lg text-sm max-w-[80%]">
            thinking...
          </div>
        )}
      </div>

      <div className="p-4 border-t border-zinc-800 flex gap-2">
        <input
          className="flex-1 bg-zinc-800 text-zinc-100 px-4 py-2 rounded-lg text-sm outline-none placeholder-zinc-500"
          placeholder="Type a message..."
          value={input}
          onChange={e => onInputChange(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && !loading && onSend()}
          disabled={loading}
        />
        <button
          onClick={onSend}
          disabled={loading || !input.trim()}
          className="bg-blue-600 hover:bg-blue-500 disabled:opacity-40 text-white px-4 py-2 rounded-lg text-sm"
        >
          Send
        </button>
      </div>
    </div>
  )
}

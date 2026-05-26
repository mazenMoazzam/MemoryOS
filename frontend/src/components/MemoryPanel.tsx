interface Props {
  memories: string[]
}

export default function MemoryPanel({ memories }: Props) {
  return (
    <div className="h-full p-4 flex flex-col">
      <h2 className="text-zinc-400 text-xs uppercase tracking-widest mb-4">
        Memories Used
      </h2>

      {memories.length === 0 ? (
        <p className="text-zinc-600 text-sm">
          No memories retrieved yet.
        </p>
      ) : (
        <ul className="space-y-2">
          {memories.map((mem, i) => (
            <li
              key={i}
              className="bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-300 text-sm"
            >
              {mem}
            </li>
          ))}
        </ul>
      )}

      <div className="mt-auto pt-4 border-t border-zinc-800">
        <p className="text-zinc-600 text-xs">
          {memories.length} memor{memories.length === 1 ? 'y' : 'ies'} retrieved from C++ engine
        </p>
      </div>
    </div>
  )
}

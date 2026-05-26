export interface Message {
  role: 'user' | 'agent'
  content: string
}

export interface ChatResponse {
  response: string
  memories_used: string[]
}

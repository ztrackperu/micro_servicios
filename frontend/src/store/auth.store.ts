import { create } from 'zustand'
import { http } from '../api/http'

type User = { id: string; email: string; nombre: string; apellido: string; rol: string }

type State = {
  user: User | null
  login: (email: string, password: string) => Promise<void>
  loadMe: () => Promise<void>
  logout: () => void
}

export const useAuth = create<State>((set) => ({
  user: null,
  async login(email, password) {
    const { data } = await http.post('/api/auth/login', { email, password })
    localStorage.setItem('token', data.access_token)
    await this.loadMe()
  },
  async loadMe() {
    const { data } = await http.get('/api/users/me')
    set({ user: data })
  },
  logout() {
    localStorage.removeItem('token')
    set({ user: null })
  }
}))

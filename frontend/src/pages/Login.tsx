import { useState } from 'react'
import { useAuth } from '../store/auth.store'
import { useNavigate } from 'react-router-dom'

export default function Login() {
  const [email,setEmail] = useState('')
  const [password,setPassword] = useState('')
  const login = useAuth(s=>s.login)
  const navigate = useNavigate()

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    await login(email,password)
    navigate('/')
  }
  return (
    <div style={{display:'grid',placeItems:'center',height:'100vh'}}>
      <form onSubmit={onSubmit} style={{display:'grid',gap:8,minWidth:300}}>
        <h2>Login</h2>
        <input placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button>Entrar</button>
      </form>
    </div>
  )
}

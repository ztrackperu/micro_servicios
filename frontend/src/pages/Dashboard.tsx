import { useEffect } from 'react'
import { useAuth } from '../store/auth.store'
import { Link } from 'react-router-dom'

export default function Dashboard() {
  const { user, loadMe, logout } = useAuth()
  useEffect(()=>{ if (!user) loadMe().catch(()=>{}) },[])
  return (
    <div style={{padding:16}}>
      <h2>Dashboard</h2>
      {user ? (
        <>
          <p>Hola, {user.nombre} {user.apellido} – Rol: {user.rol}</p>
          <button onClick={()=>logout()}>Salir</button>
          <div style={{marginTop:16}}>
            <Link to="/devices">Ver dispositivos</Link>
          </div>
        </>
      ) : (<p>No autenticado</p>)}
    </div>
  )
}

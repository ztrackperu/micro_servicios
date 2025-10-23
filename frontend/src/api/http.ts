import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE || 'http://localhost:8080'
export const http = axios.create({ baseURL })

http.interceptors.request.use(cfg => {
  const token = localStorage.getItem('token')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

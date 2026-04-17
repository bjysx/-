import axios from "axios"
import { ElMessage } from "element-plus"
import { useAuthStore } from "../store/auth"

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  timeout: 20000
})

http.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.state.accessToken) {
    config.headers.Authorization = `Bearer ${auth.state.accessToken}`
  }
  return config
})

http.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const auth = useAuthStore()
    const message = error.response?.data?.detail || error.response?.data?.message || error.message || "请求失败"
    if (error.response?.status === 401) {
      auth.clear()
      if (!window.location.pathname.includes("/login")) {
        window.location.href = "/login"
      }
    } else {
      ElMessage.error(message)
    }
    return Promise.reject(error)
  }
)

export default http

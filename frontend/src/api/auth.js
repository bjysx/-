import http from "./http"

export function login(payload) {
  return http.post("/user/login/", payload)
}

export function logout() {
  return http.post("/user/logout/")
}

export function getProfile() {
  return http.get("/user/info/")
}

export function changePassword(payload) {
  return http.post("/user/change-password/", payload)
}

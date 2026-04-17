import http from "./http"

export function getMenuTree() {
  return http.get("/system/menu/")
}

export function getDashboardData() {
  return http.get("/business/dashboard/")
}

export function getUsers() {
  return http.get("/user/users/")
}

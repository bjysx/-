import { createRouter, createWebHistory } from "vue-router"
import { routes } from "./routes"
import { getProfile } from "../api/auth"
import { getMenuTree } from "../api/system"
import { useAuthStore } from "../store/auth"

const router = createRouter({
  history: createWebHistory(),
  routes
})

let hydrated = false

async function hydrateAuthContext() {
  const auth = useAuthStore()
  if (!auth.hasToken()) {
    return false
  }
  if (hydrated && auth.state.user && auth.state.menus?.length) {
    return true
  }
  const [profile, menus] = await Promise.all([getProfile(), getMenuTree()])
  auth.setUser(profile)
  auth.setMenus(menus)
  hydrated = true
  return true
}

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (to.meta.public) {
    if (to.name === "login" && auth.hasToken()) {
      return { name: "dashboard-home" }
    }
    return true
  }
  if (!auth.hasToken()) {
    return {
      name: "login",
      query: {
        redirect: to.fullPath
      }
    }
  }
  try {
    await hydrateAuthContext()
    if (to.meta.permissionKey && !auth.canAccess(to.meta.permissionKey)) {
      return { name: "forbidden" }
    }
    return true
  } catch {
    auth.clear()
    return { name: "login" }
  }
})

export default router

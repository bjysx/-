import { reactive, readonly } from "vue"
import { menuConfig } from "../config/menu"
import { useAuthStore } from "./auth"

const THEME_KEY = "jinsyiyuan-theme"

const state = reactive({
  sidebarCollapsed: false,
  isMobile: false,
  theme: "light"
})

function updateDeviceState() {
  state.isMobile = window.innerWidth < 1024
  if (state.isMobile) {
    state.sidebarCollapsed = true
  }
}

function applyTheme(theme) {
  state.theme = theme
  document.documentElement.classList.toggle("dark", theme === "dark")
  localStorage.setItem(THEME_KEY, theme)
  useAuthStore().setTheme(theme)
}

export function initializeAppState() {
  const auth = useAuthStore()
  const preferredTheme = auth.state.user?.theme_preference || localStorage.getItem(THEME_KEY) || "light"
  updateDeviceState()
  applyTheme(preferredTheme)
  window.addEventListener("resize", updateDeviceState)
}

export function useAppStore() {
  const auth = useAuthStore()
  return {
    state: readonly(state),
    toggleSidebar(forceValue) {
      if (typeof forceValue === "boolean") {
        state.sidebarCollapsed = forceValue
        return
      }
      state.sidebarCollapsed = !state.sidebarCollapsed
    },
    toggleTheme() {
      applyTheme(state.theme === "dark" ? "light" : "dark")
    },
    availableMenus() {
      return auth.state.menus?.length ? auth.state.menus : menuConfig
    }
  }
}

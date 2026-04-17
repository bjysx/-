import { reactive, readonly } from "vue"

const LOCAL_KEY = "jinsyiyuan-auth-local"
const SESSION_KEY = "jinsyiyuan-auth-session"

const state = reactive({
  accessToken: "",
  refreshToken: "",
  remember: true,
  user: null,
  permissionKeys: [],
  buttonPermissions: {},
  menus: []
})

function parseStorage(raw) {
  if (!raw) {
    return null
  }
  try {
    return JSON.parse(raw)
  } catch {
    return null
  }
}

function persistState() {
  const payload = JSON.stringify({
    accessToken: state.accessToken,
    refreshToken: state.refreshToken,
    remember: state.remember,
    user: state.user,
    permissionKeys: state.permissionKeys,
    buttonPermissions: state.buttonPermissions,
    menus: state.menus
  })
  if (state.remember) {
    localStorage.setItem(LOCAL_KEY, payload)
    sessionStorage.removeItem(SESSION_KEY)
  } else {
    sessionStorage.setItem(SESSION_KEY, payload)
    localStorage.removeItem(LOCAL_KEY)
  }
}

export function initializeAuthState() {
  const saved = parseStorage(localStorage.getItem(LOCAL_KEY)) || parseStorage(sessionStorage.getItem(SESSION_KEY))
  if (!saved) {
    return
  }
  state.accessToken = saved.accessToken || ""
  state.refreshToken = saved.refreshToken || ""
  state.remember = saved.remember ?? true
  state.user = saved.user || null
  state.permissionKeys = saved.permissionKeys || []
  state.buttonPermissions = saved.buttonPermissions || {}
  state.menus = saved.menus || []
}

export function useAuthStore() {
  return {
    state: readonly(state),
    hasToken() {
      return Boolean(state.accessToken)
    },
    setSession(payload) {
      state.accessToken = payload.access || ""
      state.refreshToken = payload.refresh || ""
      state.remember = payload.remember ?? true
      state.user = payload.user || null
      state.permissionKeys = payload.user?.permission_keys || []
      state.buttonPermissions = payload.user?.button_permissions || {}
      persistState()
    },
    setUser(user) {
      state.user = user
      state.permissionKeys = user?.permission_keys || []
      state.buttonPermissions = user?.button_permissions || {}
      persistState()
    },
    setMenus(menus) {
      state.menus = menus || []
      persistState()
    },
    setTheme(theme) {
      if (!state.user) {
        return
      }
      state.user = {
        ...state.user,
        theme_preference: theme
      }
      persistState()
    },
    clear() {
      state.accessToken = ""
      state.refreshToken = ""
      state.user = null
      state.permissionKeys = []
      state.buttonPermissions = {}
      state.menus = []
      localStorage.removeItem(LOCAL_KEY)
      sessionStorage.removeItem(SESSION_KEY)
    },
    canAccess(pageCode) {
      if (!pageCode) {
        return true
      }
      if (!state.permissionKeys?.length) {
        return true
      }
      return state.permissionKeys.includes(pageCode)
    },
    allowedButtons(pageCode) {
      return state.buttonPermissions[pageCode] || []
    }
  }
}

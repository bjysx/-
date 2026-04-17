import { createApp } from "vue"
import * as ElementPlusIconsVue from "@element-plus/icons-vue"
import ElementPlus from "element-plus"
import "element-plus/dist/index.css"
import "./styles/index.css"
import App from "./App.vue"
import router from "./router"
import { initializeAppState } from "./store/app"
import { initializeAuthState } from "./store/auth"

const app = createApp(App)

Object.entries(ElementPlusIconsVue).forEach(([key, component]) => {
  app.component(key, component)
})

initializeAuthState()
initializeAppState()

app.use(router)
app.use(ElementPlus)
app.mount("#app")

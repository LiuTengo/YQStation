//import { createApp } from 'vue'
//import './style.css'
//import App from './App.vue'

//createApp(App).mount('#app')

import { createApp, h } from 'vue'
import App from './App.vue'
import './style.css'

import {
  create,
  NMessageProvider
} from 'naive-ui'

import router from './index'

const naive = create({})

const app = createApp({
  render() {
    return h(
      NMessageProvider,
      null,
      {
        default: () => h(App)
      }
    )
  }
})

app.use(naive)
app.use(router)

app.mount('#app')
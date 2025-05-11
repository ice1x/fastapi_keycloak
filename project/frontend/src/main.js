import { createApp } from 'vue'
import App from './App.vue'
import Keycloak from 'keycloak-js'

const initAuth = async () => {
  const keycloak = new Keycloak({
    url: 'http://localhost:8080',
    realm: 'demo-realm',
    clientId: 'frontend-client'
  })

  try {
    // Completely disable all iframe mechanisms
    const auth = await keycloak.init({
      onLoad: 'login-required',
      flow: 'standard',
      pkceMethod: 'S256',
      checkLoginIframe: false
    })

    if (auth) {
      const app = createApp(App)
      app.config.globalProperties.$keycloak = keycloak
      app.mount('#app')
    } else {
      window.location.reload()
    }
  } catch (err) {
    console.error('Auth failed:', err)
    document.getElementById('app').innerHTML = `
      <div style="padding: 20px; text-align: center;">
        <h2>Authorization Error</h2>
        <p>${err.message || 'Unknown error'}</p>
        <button style="padding: 8px 16px;" onclick="window.location.href='/'">
          Try Again
        </button>
      </div>
    `
  }
}

initAuth()

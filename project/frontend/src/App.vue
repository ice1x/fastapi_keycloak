// frontend/src/App.vue
<template>
  <div>
    <h1>Welcome!</h1>
    <p>User: {{ username }}</p>
    <p>Roles: {{ roles }}</p>
    <button @click="onLogout">Logout</button>
    <button @click="fetchItems">Load Items</button>

    <div>
      <h3>Token Debug:</h3>
      <pre>{{ tokenDebug }}</pre>
    </div>

    <div v-if="isAdmin">
      <h2>Create Item (admin only)</h2>
      <input v-model="newItem.name" placeholder="Item name" />
      <input v-model="newItem.description" placeholder="Item description" />
      <button @click="createItem">Create</button>
    </div>

    <ul>
      <li v-for="item in items" :key="item.id">
        {{ item.name }} — {{ item.description }}
        <button v-if="isAdmin" @click="deleteItem(item.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { computed, ref, getCurrentInstance } from 'vue'

const { appContext } = getCurrentInstance()
const keycloak = appContext.config.globalProperties.$keycloak

const username = computed(() => keycloak?.tokenParsed?.preferred_username || 'unknown')
const roles = computed(() => keycloak?.tokenParsed?.realm_access?.roles?.join(', ') || 'none')
const isAdmin = computed(() => keycloak?.tokenParsed?.realm_access?.roles?.includes('admin'))
const tokenDebug = computed(() => JSON.stringify(keycloak?.tokenParsed, null, 2))

if (!isAdmin.value) {
  console.warn('User does not have admin role')
}

function onLogout() {
  if (keycloak) {
    keycloak.logout({ redirectUri: window.location.origin })
  }
}

const items = ref([])
const newItem = ref({ name: '', description: '' })

async function fetchItems() {
  try {
    const response = await fetch('http://localhost:8000/items', {
      headers: {
        Authorization: `Bearer ${keycloak.token}`
      }
    })

    if (!response.ok) {
      throw new Error(`Error ${response.status}`)
    }

    items.value = await response.json()
  } catch (err) {
    console.error('Failed to fetch items:', err)
  }
}

async function createItem() {
  try {
    console.log('Creating item with roles:', keycloak.tokenParsed?.realm_access?.roles)

    const response = await fetch('http://localhost:8000/items', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${keycloak.token}`
      },
      body: JSON.stringify(newItem.value)
    })

    if (!response.ok) {
      throw new Error(`Error ${response.status}`)
    }

    const item = await response.json()
    items.value.push(item)
    newItem.value = { name: '', description: '' }
  } catch (err) {
    console.error('Failed to create item:', err)
  }
}

async function deleteItem(itemId) {
  try {
    const response = await fetch(`http://localhost:8000/items/${itemId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${keycloak.token}`
      }
    })

    if (!response.ok) {
      throw new Error(`Error ${response.status}`)
    }

    items.value = items.value.filter(item => item.id !== itemId)
  } catch (err) {
    console.error('Failed to delete item:', err)
  }
}
</script>

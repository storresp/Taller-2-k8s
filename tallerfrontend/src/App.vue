<script setup>
import { ref } from 'vue'

// Variable reactiva para el valor del input de texto
const inputValue = ref('')

// Lista reactiva que almacena todos los valores registrados (se actualiza desde el backend)
const itemList = ref([])

// ─────────────────────────────────────────────────────────────────────────────
// NOTA BACKEND: La URL base del backend Django.
// Actualmente el backend solo tiene el endpoint GET /polls/ que devuelve
// "Hello, world." y NO guarda ni devuelve datos de la base de datos.
//
// Para que este frontend funcione completamente, el backend necesita:
//   1. Un endpoint POST /polls/items/ → que reciba { "value": "..." }
//      y lo guarde en la base de datos.
//   2. Un endpoint GET /polls/items/ → que devuelva la lista de todos
//      los items guardados en formato JSON: [{ "id": 1, "value": "..." }, ...]
//   3. Habilitar CORS en Django (instalar django-cors-headers y configurarlo
//      en settings.py) para que Vue pueda hacer peticiones al backend.
//
// URL A AJUSTAR cuando el backend esté listo:
const API_BASE_URL = 'http://localhost:8000/polls'
// ─────────────────────────────────────────────────────────────────────────────

// Función que se ejecuta al presionar el botón
async function handleSubmit() {
  const value = inputValue.value.trim()
  if (!value) return

  // ─────────────────────────────────────────────────────────────────────────
  // NOTA BACKEND: Esta llamada POST requiere que el backend tenga implementado
  // el endpoint POST /polls/items/ que acepte JSON { "value": "..." } y lo
  // guarde en la base de datos. Actualmente ese endpoint NO existe en el back.
  // ─────────────────────────────────────────────────────────────────────────
  try {
    await fetch(`${API_BASE_URL}/items/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ value: value })
    })

    // Limpiar el input después de enviar
    inputValue.value = ''

    // Recargar la lista desde el backend después de guardar
    await loadItems()
  } catch (error) {
    // ─────────────────────────────────────────────────────────────────────
    // NOTA BACKEND: Si el backend no está corriendo o el endpoint no existe,
    // la petición fallará y caerá aquí. Una vez el backend esté completo,
    // este catch solo debería manejar errores reales de red.
    // ─────────────────────────────────────────────────────────────────────
    console.error('Error al enviar al backend:', error)
  }
}

// Función para obtener todos los items guardados desde el backend
async function loadItems() {
  // ─────────────────────────────────────────────────────────────────────────
  // NOTA BACKEND: Esta llamada GET requiere que el backend tenga implementado
  // el endpoint GET /polls/items/ que devuelva un array JSON con todos los
  // items guardados. Actualmente ese endpoint NO existe en el back.
  // ─────────────────────────────────────────────────────────────────────────
  try {
    const response = await fetch(`${API_BASE_URL}/items/`)
    const data = await response.json()
    // Se espera que el backend devuelva un array: [{ id, value }, ...]
    itemList.value = data
  } catch (error) {
    console.error('Error al cargar items del backend:', error)
  }
}
</script>

<template>
  <!-- Fondo completo de la página -->
  <div class="page-bg">
    <div class="card">

      <!-- Título principal de la app -->
      <h1 class="title"> DEATH NOTE</h1>
      <div class="form-section">

        <label for="main-input" class="main-label">
          Nombre:
        </label>

        <!-- Input de texto donde el usuario escribe el valor a registrar -->
        <div class="input-row">
          <input
            id="main-input"
            v-model="inputValue"
            type="text"
            class="main-input"
            placeholder="Escribe un nombre..."
            @keyup.enter="handleSubmit"
          />

          <!-- Botón que envía el valor al backend -->
          <button class="submit-btn" @click="handleSubmit">
             Guardar
          </button>
        </div>
      </div>

      <!-- Separador -->
      <div class="divider"></div>

      <!-- Lista dinámica de todos los valores registrados en la base de datos -->
      <div class="list-section">
        <h2 class="list-title"> Nombres registrados</h2>

        <!--
          NOTA BACKEND: Esta lista se pobla con los datos que devuelve el backend.
          Mientras el backend esté incompleto, la lista permanecerá vacía.
        -->
        <ul v-if="itemList.length > 0" class="item-list">
          <li
            v-for="item in itemList"
            :key="item.id"
            class="item"
          >
            <span class="item-icon">☠️</span>
            {{ item.value }}
          </li>
        </ul>

        <!-- Mensaje cuando no hay datos aún -->
        <div v-else class="empty-state">
          <span class="empty-icon">📖</span>
          <p class="empty-msg">El cuaderno está vacío...</p>
        </div>
      </div>

    </div>
  </div>
</template>

<style>
/* Reset global y fuente */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Inter', sans-serif;
  background: #0d0d0d;
}
</style>

<style scoped>
/* ── Fondo de página centrado ── */
.page-bg {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(ellipse at top, #1a0a2e 0%, #0d0d0d 70%);
  padding: 24px;
}

/* ── Tarjeta principal ── */
.card {
  width: 100%;
  max-width: 480px;
  background: linear-gradient(145deg, #131313, #1c1c1c);
  border: 1px solid #2a2a2a;
  border-radius: 20px;
  padding: 40px 36px;
  box-shadow:
    0 0 0 1px rgba(180, 0, 0, 0.15),
    0 20px 60px rgba(0, 0, 0, 0.6),
    0 0 80px rgba(120, 0, 0, 0.08);
}

/* ── Título ── */
.title {
  font-size: 2rem;
  font-weight: 700;
  color: #e8e8e8;
  text-align: center;
  letter-spacing: 0.05em;
  margin-bottom: 6px;
}



/* ── Formulario ── */
.form-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 28px;
}

.main-label {
  font-weight: 600;
  color: #aaa;
  font-size: 0.82rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.input-row {
  display: flex;
  gap: 10px;
}

.main-input {
  flex: 1;
  padding: 12px 16px;
  background: #0d0d0d;
  border: 1px solid #2e2e2e;
  border-radius: 10px;
  font-size: 0.95rem;
  color: #e0e0e0;
  outline: none;
  font-family: 'Inter', sans-serif;
  transition: border-color 0.25s, box-shadow 0.25s;
}

.main-input::placeholder {
  color: #444;
}

.main-input:focus {
  border-color: #8b0000;
  box-shadow: 0 0 0 3px rgba(139, 0, 0, 0.2);
}

.submit-btn {
  padding: 12px 20px;
  background: linear-gradient(135deg, #8b0000, #b00020);
  color: #f0c0c0;
  border: none;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  transition: all 0.2s ease;
  white-space: nowrap;
  box-shadow: 0 4px 15px rgba(139, 0, 0, 0.35);
}

.submit-btn:hover {
  background: linear-gradient(135deg, #a00000, #cc0025);
  box-shadow: 0 6px 20px rgba(139, 0, 0, 0.5);
  transform: translateY(-1px);
}

.submit-btn:active {
  transform: translateY(0);
}

/* ── Separador ── */
.divider {
  height: 1px;
  background: linear-gradient(to right, transparent, #2a2a2a, transparent);
  margin-bottom: 28px;
}

/* ── Lista ── */
.list-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #666;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 16px;
}

.item-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: #0f0f0f;
  border: 1px solid #222;
  border-radius: 10px;
  color: #d0d0d0;
  font-size: 0.95rem;
  transition: border-color 0.2s, background 0.2s;
}

.item:hover {
  background: #141414;
  border-color: #3a1a1a;
}

.item-icon {
  font-size: 1rem;
  flex-shrink: 0;
}

/* ── Estado vacío ── */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 32px 0;
}

.empty-icon {
  font-size: 2.5rem;
  opacity: 0.3;
}

.empty-msg {
  color: #444;
  font-style: italic;
  font-size: 0.88rem;
}
</style>

<script setup>
import { ref, onMounted } from 'vue'

// Variable reactiva para el valor del input de texto
const inputValue = ref('')

// Lista reactiva con todos los registros devueltos por el backend
const itemList = ref([])

// Indicador de estado: 'idle' | 'loading' | 'error'
const status = ref('idle')

// URL base del backend Django — usando ruta relativa para que el proxy
// de Vite redirija la petición a http://localhost:8000 sin errores de CORS
const API_BASE_URL = '/polls'

// ─── Cargar la lista al montar el componente ───────────────────────────────
onMounted(() => {
  loadItems()
})

// ─── Enviar un nuevo registro al backend ──────────────────────────────────
async function handleSubmit() {
  const value = inputValue.value.trim()
  if (!value) return

  status.value = 'loading'
  try {
    // POST /polls/answers/ — campo requerido por el modelo Django: "answer_text"
    const res = await fetch(`${API_BASE_URL}/answers/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answer_text: value })
    })

    if (!res.ok) {
      console.error('Error del servidor:', await res.text())
      status.value = 'error'
      return
    }

    inputValue.value = ''
    status.value = 'idle'

    // Recargar la lista actualizada desde el backend
    await loadItems()
  } catch (error) {
    console.error('Error de red al enviar:', error)
    status.value = 'error'
  }
}

// ─── Obtener todos los registros guardados ────────────────────────────────
async function loadItems() {
  try {
    // GET /polls/answers/ — devuelve: [{ id, answer_text, pub_date }, ...]
    const response = await fetch(`${API_BASE_URL}/answers/`)
    const data = await response.json()
    itemList.value = data
  } catch (error) {
    console.error('Error de red al cargar items:', error)
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
          <button class="submit-btn" :disabled="status === 'loading'" @click="handleSubmit">
            {{ status === 'loading' ? 'Guardando...' : 'Guardar' }}
          </button>
        </div>
      </div>

      <!-- Separador -->
      <div class="divider"></div>

      <!-- Lista dinámica de todos los valores registrados en la base de datos -->
      <div class="list-section">
        <h2 class="list-title"> Nombres registrados</h2>

        <!-- Lista poblada con los datos del backend: GET /polls/answers/ -->
        <ul v-if="itemList.length > 0" class="item-list">
          <li
            v-for="item in itemList"
            :key="item.id"
            class="item"
          >
            <div class="item-content">
              <!-- item.answer_text es el campo del modelo Django Answer -->
              <span class="item-name">{{ item.answer_text }}</span>
              <span class="item-date">{{ item.pub_date }}</span>
            </div>
          </li>
        </ul>

        <!-- Mensaje cuando no hay datos aún -->
        <div v-else class="empty-state">
          <span class="empty-icon"></span>
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

.submit-btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
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
  padding: 12px 16px;
  background: #0f0f0f;
  border: 1px solid #222;
  border-radius: 10px;
  color: #d0d0d0;
  transition: border-color 0.2s, background 0.2s;
}

.item:hover {
  background: #141414;
  border-color: #3a1a1a;
}

/* Contenedor flex para nombre + fecha */
.item-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  width: 100%;
}

.item-name {
  font-size: 0.95rem;
  color: #e0e0e0;
  font-weight: 500;
}

.item-date {
  font-size: 0.72rem;
  color: #555;
  white-space: nowrap;
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

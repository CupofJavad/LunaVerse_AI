<template>
  <div class="event-wizard">
    <header>
      <h1>Create New Event</h1>
      <button @click="$router.push('/dashboard')">Cancel</button>
    </header>
    <main>
      <form @submit.prevent="handleSubmit">
        <div class="step">
          <h2>Event Details</h2>
          <div class="form-group">
            <label>Event Name *</label>
            <input v-model="eventSpec.event_name" required />
          </div>
          <div class="form-group">
            <label>Client Name *</label>
            <input v-model="eventSpec.client_name" required />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Start Date *</label>
              <input v-model="eventSpec.start_date" type="date" required />
            </div>
            <div class="form-group">
              <label>End Date *</label>
              <input v-model="eventSpec.end_date" type="date" required />
            </div>
          </div>
          <div class="form-group">
            <label>Venue *</label>
            <input v-model="eventSpec.venue" required />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>City *</label>
              <input v-model="eventSpec.city" required />
            </div>
            <div class="form-group">
              <label>State *</label>
              <input v-model="eventSpec.state" required />
            </div>
            <div class="form-group">
              <label>Country *</label>
              <input v-model="eventSpec.country" required />
            </div>
          </div>
          <div class="form-group">
            <label>Timezone *</label>
            <input v-model="eventSpec.timezone" placeholder="America/New_York" required />
          </div>
        </div>

        <div class="step">
          <h2>Rooms</h2>
          <div v-for="(room, index) in eventSpec.rooms" :key="index" class="room-card">
            <h3>Room {{ index + 1 }}</h3>
            <div class="form-group">
              <label>Room Name *</label>
              <input v-model="room.name" required />
            </div>
            <div class="form-group">
              <label>Room Type *</label>
              <select v-model="room.type" required>
                <option value="GS">General Session</option>
                <option value="Breakout">Breakout</option>
                <option value="Panel">Panel</option>
                <option value="Workshop">Workshop</option>
                <option value="Expo">Expo</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div class="form-group">
              <label>Capacity *</label>
              <input v-model.number="room.capacity" type="number" required />
            </div>
            <button type="button" @click="removeRoom(index)" class="btn-danger">Remove Room</button>
          </div>
          <button type="button" @click="addRoom" class="btn-secondary">Add Room</button>
        </div>

        <button type="submit" :disabled="loading" class="btn-primary">Generate Plan</button>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </main>
  </div>
</template>

<script>
import { generatePlan } from '../api/plan'
import { useRouter } from 'vue-router'

export default {
  name: 'EventWizard',
  data() {
    return {
      eventSpec: {
        event_name: '',
        client_name: '',
        start_date: '',
        end_date: '',
        venue: '',
        city: '',
        state: '',
        country: 'USA',
        timezone: 'America/New_York',
        rooms: [{
          name: '',
          type: 'GS',
          capacity: 100,
          days_active: [],
          audio: {},
          video: {},
          lighting: {},
          staging: {},
          power: {},
          schedule: {}
        }]
      },
      loading: false,
      error: ''
    }
  },
  setup() {
    const router = useRouter()
    return { router }
  },
  methods: {
    addRoom() {
      this.eventSpec.rooms.push({
        name: '',
        type: 'GS',
        capacity: 100,
        days_active: [],
        audio: {},
        video: {},
        lighting: {},
        staging: {},
        power: {},
        schedule: {}
      })
    },
    removeRoom(index) {
      this.eventSpec.rooms.splice(index, 1)
    },
    async handleSubmit() {
      this.loading = true
      this.error = ''
      
      try {
        const response = await generatePlan(this.eventSpec)
        // Extract event_id from response or create event first
        const eventId = response.event_id || response.event?.event_id
        if (eventId) {
          this.router.push(`/events/${eventId}/plan`)
        } else {
          this.error = 'Failed to create event'
        }
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to generate plan'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.event-wizard {
  min-height: 100vh;
  background: #f5f5f5;
}

header {
  background: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

main {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 8px;
}

.step {
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

input, select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.room-card {
  border: 1px solid #ddd;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.btn-primary, .btn-secondary, .btn-danger {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
}

.btn-primary {
  background: #667eea;
  color: white;
  width: 100%;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>


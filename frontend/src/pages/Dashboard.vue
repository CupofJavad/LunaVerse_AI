<template>
  <div class="dashboard">
    <header>
      <h1>Lunaverse Show Brain</h1>
      <button @click="handleLogout">Logout</button>
    </header>
    <main>
      <div class="actions">
        <button @click="createNewEvent" class="btn-primary">New Event</button>
      </div>
      <div class="events-list">
        <h2>Recent Events</h2>
        <div v-if="loading">Loading...</div>
        <div v-else-if="events.length === 0">No events found</div>
        <div v-else class="events-grid">
          <div v-for="event in events" :key="event.id" class="event-card" @click="viewEvent(event.id)">
            <h3>{{ event.event_name }}</h3>
            <p>{{ event.client_name }}</p>
            <p class="date">{{ event.start_date }} - {{ event.end_date }}</p>
            <p class="venue">{{ event.venue }}, {{ event.city }}</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { listEvents } from '../api/events'
import { useRouter } from 'vue-router'

export default {
  name: 'Dashboard',
  data() {
    return {
      events: [],
      loading: true
    }
  },
  setup() {
    const router = useRouter()
    return { router }
  },
  async mounted() {
    await this.loadEvents()
  },
  methods: {
    async loadEvents() {
      try {
        const response = await listEvents()
        this.events = response.events
      } catch (err) {
        console.error('Failed to load events:', err)
      } finally {
        this.loading = false
      }
    },
    createNewEvent() {
      this.router.push('/events/new')
    },
    viewEvent(eventId) {
      this.router.push(`/events/${eventId}/plan`)
    },
    handleLogout() {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      this.router.push('/login')
    }
  }
}
</script>

<style scoped>
.dashboard {
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
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem;
}

.actions {
  margin-bottom: 2rem;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

.events-list h2 {
  margin-bottom: 1rem;
}

.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.event-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
}

.event-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.event-card h3 {
  margin-bottom: 0.5rem;
  color: #333;
}

.event-card p {
  color: #666;
  margin-bottom: 0.25rem;
}

.event-card .date {
  font-weight: 600;
  color: #667eea;
}
</style>


<template>
  <div class="plan-viewer">
    <header>
      <h1>{{ plan?.event_name || 'Event Plan' }}</h1>
      <div class="actions">
        <button @click="exportEquipment" class="btn-secondary">Export Equipment CSV</button>
        <button @click="exportCrew" class="btn-secondary">Export Crew CSV</button>
        <button @click="exportSummary" class="btn-secondary">Export Summary</button>
        <button @click="$router.push('/dashboard')">Back to Dashboard</button>
      </div>
    </header>
    <main v-if="loading">
      <div class="loading">Loading plan...</div>
    </main>
    <main v-else-if="plan">
      <div class="summary-section">
        <h2>Summary</h2>
        <p>{{ plan.summary }}</p>
        <h3>Assumptions</h3>
        <ul>
          <li v-for="(assumption, idx) in plan.assumptions" :key="idx">{{ assumption }}</li>
        </ul>
        <h3>Trucking</h3>
        <p>Estimated Trucks: {{ plan.trucking?.estimated_trucks || 0 }}</p>
        <p>Total Weight: {{ plan.trucking?.weight_total_lbs || 0 }} lbs</p>
      </div>
      
      <div class="rooms-section">
        <h2>Rooms</h2>
        <div v-for="room in plan.rooms" :key="room.room_id" class="room-section">
          <h3>{{ room.name }}</h3>
          
          <div class="equipment-section">
            <h4>Equipment</h4>
            <table>
              <thead>
                <tr>
                  <th>Item Code</th>
                  <th>Name</th>
                  <th>Qty</th>
                  <th>Product Group</th>
                  <th>Weight</th>
                  <th>Notes</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, idx) in room.equipment" :key="idx">
                  <td>{{ item.item_code }}</td>
                  <td>{{ item.name }}</td>
                  <td>{{ item.qty }}</td>
                  <td>{{ item.product_group_name }}</td>
                  <td>{{ item.weight_total || 0 }} lbs</td>
                  <td>{{ item.notes }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div class="crew-section">
            <h4>Crew</h4>
            <table>
              <thead>
                <tr>
                  <th>Role</th>
                  <th>Qty</th>
                  <th>Hours In</th>
                  <th>Hours Show</th>
                  <th>Hours Out</th>
                  <th>Bill Rate</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(member, idx) in room.crew" :key="idx">
                  <td>{{ member.role }}</td>
                  <td>{{ member.qty }}</td>
                  <td>{{ member.hours_in || 0 }}</td>
                  <td>{{ member.hours_show || 0 }}</td>
                  <td>{{ member.hours_out || 0 }}</td>
                  <td>${{ member.bill_rate || 0 }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { getEventPlan, exportEquipmentCSV, exportCrewCSV, exportSummary } from '../api/plan'
import { useRoute } from 'vue-router'

export default {
  name: 'PlanViewer',
  data() {
    return {
      plan: null,
      loading: true
    }
  },
  setup() {
    const route = useRoute()
    return { route }
  },
  async mounted() {
    await this.loadPlan()
  },
  methods: {
    async loadPlan() {
      try {
        const eventId = this.route.params.id
        const response = await getEventPlan(eventId)
        this.plan = response.event_plan
      } catch (err) {
        console.error('Failed to load plan:', err)
      } finally {
        this.loading = false
      }
    },
    async exportEquipment() {
      try {
        const eventId = this.route.params.id
        const blob = await exportEquipmentCSV(eventId)
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `equipment_${eventId}.csv`
        a.click()
      } catch (err) {
        console.error('Export failed:', err)
      }
    },
    async exportCrew() {
      try {
        const eventId = this.route.params.id
        const blob = await exportCrewCSV(eventId)
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `crew_${eventId}.csv`
        a.click()
      } catch (err) {
        console.error('Export failed:', err)
      }
    },
    async exportSummary() {
      try {
        const eventId = this.route.params.id
        const blob = await exportSummary(eventId)
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `summary_${eventId}.txt`
        a.click()
      } catch (err) {
        console.error('Export failed:', err)
      }
    }
  }
}
</script>

<style scoped>
.plan-viewer {
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

.actions {
  display: flex;
  gap: 0.5rem;
}

main {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem;
}

.summary-section, .rooms-section {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.room-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background: #f8f9fa;
  font-weight: 600;
}

.btn-secondary {
  padding: 0.5rem 1rem;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.loading {
  text-align: center;
  padding: 2rem;
}
</style>


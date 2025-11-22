import client from './client'

export const generatePlan = async (eventSpec, eventId = null) => {
  const response = await client.post('/plan-event', eventSpec, {
    params: eventId ? { event_id: eventId } : {}
  })
  return response.data
}

export const getEventPlan = async (eventId) => {
  const response = await client.get(`/plan-event/${eventId}`)
  return response.data
}

export const exportEquipmentCSV = async (eventId) => {
  const response = await client.get(`/export/equipment-csv/${eventId}`, {
    responseType: 'blob'
  })
  return response.data
}

export const exportCrewCSV = async (eventId) => {
  const response = await client.get(`/export/crew-csv/${eventId}`, {
    responseType: 'blob'
  })
  return response.data
}

export const exportSummary = async (eventId) => {
  const response = await client.get(`/export/summary/${eventId}`, {
    responseType: 'blob'
  })
  return response.data
}


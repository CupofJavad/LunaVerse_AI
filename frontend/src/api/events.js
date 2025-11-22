import client from './client'

export const createEvent = async (eventSpec) => {
  const response = await client.post('/events', eventSpec)
  return response.data
}

export const getEvent = async (eventId) => {
  const response = await client.get(`/events/${eventId}`)
  return response.data
}

export const listEvents = async (page = 1, limit = 20, search = '') => {
  const response = await client.get('/events', {
    params: { page, limit, search }
  })
  return response.data
}


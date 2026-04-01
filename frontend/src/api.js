import axios from 'axios'

const client = axios.create({ baseURL: '/api', timeout: 30000 })

export async function fetchOverview()    { return (await client.get('/overview')).data }
export async function fetchMap()         { return (await client.get('/map')).data }
export async function fetchTrends()      { return (await client.get('/trends')).data }
export async function postChat(prompt)   { return (await client.post('/chat', { prompt })).data }
export async function fetchHealth()      { return (await client.get('/health')).data }

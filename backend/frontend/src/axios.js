import axios from 'axios'

const API_URL = axios.create({
    baseURL:'http://127.0.0.1:8000/api/',
    timeout: 1000,
})

const API_GeoJSON = axios.create({
    baseURL:'http://127.0.0.1:8000/api/data.geojson',
    timeout: 1000,
})


export { API_URL, API_GeoJSON}

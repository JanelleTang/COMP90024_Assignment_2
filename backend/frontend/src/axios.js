import axios from 'axios'

const getAPI = axios.create({
    baseURL:'http://127.0.0.1:8000',
    timeout: 1000,
})

async function status() {
    const url = "https://api.com";
    let response = await axios.get(url);
    return response.data;
  }
  
  status().then((data) => console.log(data));
  
export { getAPI }
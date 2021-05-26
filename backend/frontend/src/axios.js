 
// # ============= COMP90024 - Assignment 2 ============= #
// #                               
// # The University of Melbourne           
// # Team 37
// #
// # ** Authors: **
// # 
// # JJ Burke              1048105
// # Janelle Tang          694209
// # Shuang Qiu            980433
// # Declan Baird-Watson   640975
// # Avinash Rao           1024577 
// # 
// # Location: Melbourne
// # ==================================================== #

import axios from 'axios'

const getAPI = axios.create({
    baseURL:'http://172.26.134.122:8000',
    timeout: 1000,
})

async function status() {
    const url = "https://api.com";
    let response = await axios.get(url);
    return response.data;
  }
  
  status().then((data) => console.log(data));
  
export { getAPI }
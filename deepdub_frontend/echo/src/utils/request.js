import axios from 'axios';

//export const baseUrl = 'http://192.168.100.69:8001/'
export const baseUrl = 'http://baadal.sytes.net:8001/'
//export const baseUrl = 'http://localhost:8001/'

const request = axios.create({
  baseURL: baseUrl,
  
  //0 means wait forever... that's what we want.
  timeout: 0,
});

export default request;

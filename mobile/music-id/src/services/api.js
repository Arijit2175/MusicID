import axios from "axios";

const api = axios.create({
  baseURL: "http://YOUR_BACKEND_IP:5000",  
  timeout: 5000
});

export default api;

import React from "react";
import axios from 'axios';
const API_URL = '/bg_rec';

export default class BGRecommenderService {
	config = {'headers': {'Content-Type': 'application/json'}};
	
	getGameList() {
        const url = `${API_URL}/api/game/`;
        return axios.get(url, this.config).then(response => response.data);
    }
	
    getGameDetail(id) {
        const url = `${API_URL}/api/game/${id}/`;
        return axios.get(url, this.config).then(response => response.data);
    }
}

export const ServiceContext = React.createContext(null);
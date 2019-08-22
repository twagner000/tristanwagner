import React from "react";
import axios from 'axios';
const API_URL = '/timetracker';

export default class TimeTrackerService {
	config = {'headers': {'Content-Type': 'application/json'}};
	
	getToken() {
		const url = `/accounts/auth-token/`;
        return axios.get(url).then(response => this.config['headers']['Authorization'] = 'Token ' + response.data.token);
	}
	
    getRecentEntries() {
        const url = `${API_URL}/api/entry/recent/`;
        return axios.get(url, this.config).then(response => response.data);
    }
	
    getEntry(id) {
        const url = `${API_URL}/api/entry/${id}/`;
        return axios.get(url, this.config).then(response => response.data);
    }
	
	updateEntry(entry){
        const url = `${API_URL}/api/entry/${entry.id}/`;
        return axios.put(url, entry, this.config);
    }
	
    createEntry(entry){
        const url = `${API_URL}/api/entry/`;
        return axios.post(url, entry, this.config);
    }
	
    getTasks() {
        const url = `${API_URL}/api/task/`;
        return axios.get(url, this.config).then(response => response.data);
    }
	
	deleteEntry(id){
        const url = `${API_URL}/api/entry/${id}`;
        return axios.delete(url, this.config);
    }
	
    getTimePeriodSummary(per_start,per_end) {
        const url = `${API_URL}/api/summary/${per_start}-to-${per_end}/`;
        return axios.get(url, this.config).then(response => response.data);
    }
}

export const ServiceContext = React.createContext(null);
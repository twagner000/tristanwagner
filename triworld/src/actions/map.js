import { REQUEST_WORLD_LIST, RECEIVE_WORLD_LIST } from "../constants/action-types";
import { REQUEST_WORLD, RECEIVE_WORLD } from "../constants/action-types";
import { SELECT_FACE, SELECT_MAJORTRI, SELECT_MINORTRI } from "../constants/action-types";



export const fetchWorldList = () => {
    return dispatch => {
		dispatch({type: REQUEST_WORLD_LIST});
		
		let headers = {"Content-Type": "application/json"};
		return fetch(`/triworld/api/world/`, {headers, })
			.then(response => response.json())
			.then(worlds => dispatch({type: RECEIVE_WORLD_LIST, worlds}));
    }
}

export const fetchWorld = (id, history) => {
    return dispatch => {
		dispatch({type: REQUEST_WORLD});
		
		let headers = {"Content-Type": "application/json"};
		return fetch(`/triworld/api/world/${id}/`, {headers, })
			.then(response => response.json())
			.then(world => {
				return dispatch({type: RECEIVE_WORLD, world});
			});
    }
}

export const selectFace = (id) => ({type: SELECT_FACE, id});

export const selectMajorTri = (id) => ({type: SELECT_MAJORTRI, id});

export const selectMinorTri = (id) => ({type: SELECT_MINORTRI, id});
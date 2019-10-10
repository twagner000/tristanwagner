import { REQUEST_FACE, RECEIVE_FACE, REQUEST_WORLD_LIST, RECEIVE_WORLD_LIST, SELECT_MAJORTRI } from "../constants/action-types";

export const fetchFace = (id) => {
    return (dispatch, getState) => {
		dispatch({type: REQUEST_FACE, id});
		
		const faces = getState().map.faces;
		if (id in faces) {
			dispatch({type: RECEIVE_FACE, face: faces[id], from_cache: true});
		} else {
			let headers = {"Content-Type": "application/json"};
			/*
			return fetch(`/triworld/api/face/${id}/`, {headers, })
				.then(response => response.json())
				.then(face => dispatch({type: RECEIVE_FACE, face, from_cache: false}));
			*/
			return fetch(`/triworld/api/face/${id}/clear_cache/`, {headers, })
				.then(response => {
					return fetch(`/triworld/api/face/${id}/`, {headers, })
						.then(response => response.json())
						.then(face => dispatch({type: RECEIVE_FACE, face, from_cache: false}));
				});
		}
    }
}

export const fetchWorldList = () => {
    return dispatch => {
		dispatch({type: REQUEST_WORLD_LIST});
		
		let headers = {"Content-Type": "application/json"};
		return fetch(`/triworld/api/world/`, {headers, })
			.then(response => response.json())
			.then(worlds => dispatch({type: RECEIVE_WORLD_LIST, worlds}));
    }
}

export const selectMajorTri = (id) => {
	return {type: SELECT_MAJORTRI, id};
}
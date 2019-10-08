import { SHOW_FACE, FETCH_FACE_REQUEST, FETCH_FACE_SUCCESS } from "../constants/action-types";

export const startFaceRequest = () => {
	return {type: FETCH_FACE_REQUEST};
}

export const showFace = (id) => {
	return {type: SHOW_FACE, id};
}

export const fetchFace = (world_id, id) => {
    return dispatch => {
        let headers = {"Content-Type": "application/json"};
        return fetch(`/triworld/api/world/${world_id}/face/${id}`, {headers, })
            .then(res => res.json())
            .then(face => {
                return dispatch({
                    type: FETCH_FACE_SUCCESS,
                    face
                })
            })
    }
}
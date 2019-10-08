import { SHOW_FACE, FETCH_FACE_REQUEST, FETCH_FACE_SUCCESS } from "../constants/action-types";

const initialState = {
	isFetchingFace: false,
	activeFace: null,
	faces: {},
};


export default function mapface(state=initialState, action) {
	let newState = Object.assign({},state);
	switch (action.type) {
		case SHOW_FACE:
			newState.activeFace = state.faces[action.id];
			return newState;
			
		case FETCH_FACE_REQUEST:
			newState.isFetchingFace = true;
			return newState;
			
		case FETCH_FACE_SUCCESS:
			newState.faces = Object.assign({}, state.faces);
			newState.faces[action.face.id] = action.face;
			newState.activeFace = action.face;
			newState.isFetchingFace = false;
			return newState;
		
		default:
            return state;
	}
}
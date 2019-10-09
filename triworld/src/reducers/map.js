import { REQUEST_FACE, RECEIVE_FACE, REQUEST_WORLD_LIST, RECEIVE_WORLD_LIST } from "../constants/action-types";

const initialState = {
	isFetchingFace: false,
	activeFace: null,
	faces: {},
	isFetchingWorldList: false,
	worlds: [],
};


export default function map(state=initialState, action) {
	let newState = Object.assign({},state);
	switch (action.type) {
		case REQUEST_FACE:
			newState.isFetchingFace = true;
			return newState;
		
		case RECEIVE_FACE:
			newState.activeFace = action.face;
			newState.isFetchingFace = false;
			if (!action.from_cache) {
				newState.faces = Object.assign({}, state.faces);
				newState.faces[action.face.id] = action.face;
			}
			return newState;
			
		case REQUEST_WORLD_LIST:
			newState.isFetchingWorldList = true;
			return newState;
		
		case RECEIVE_WORLD_LIST:
			newState.isFetchingWorldList = false;
			newState.worlds = action.worlds;
			return newState;
		
		default:
            return state;
	}
}
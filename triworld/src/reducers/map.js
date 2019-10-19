import { REQUEST_WORLD_LIST, RECEIVE_WORLD_LIST } from "../constants/action-types";
import { REQUEST_WORLD, RECEIVE_WORLD } from "../constants/action-types";
import { SELECT_FACE, SELECT_MAJORTRI, SELECT_MINORTRI } from "../constants/action-types";

const initialState = {
	isFetchingWorldList: false,
	worlds: [],
	isFetchingWorld: false,
	world: null,
	currentFace: null,
	currentMajorTri: null,
	currentMinorTri: null,
};


/*const findMajorTri = (faces,majortri_id) => {
	for (const face of faces) {
		for (const mjtri of face.majortri_set) {
			if (mjtri.id === majortri_id) {
				return mjtri;
			}
		}
	}
	return null;
};*/

/*const findMajorTri = (world,majortri_id) => {
	if (world && world.majortris && getProperty(world.majortris,majortri_id) {
		return getProperty(world.majortris,majortri_id);
	}
	return null;
};*/


export default function map(state=initialState, action) {
	let newState = Object.assign({},state);
	switch (action.type) {
		case REQUEST_WORLD_LIST:
			newState.isFetchingWorldList = true;
			return newState;
		
		case RECEIVE_WORLD_LIST:
			newState.isFetchingWorldList = false;
			newState.worlds = action.worlds;
			return newState;
			
		case REQUEST_WORLD:
			newState.isFetchingWorld = true;
			return newState;
		
		case RECEIVE_WORLD:
			newState.isFetchingWorld = false;
			newState.world = action.world;
			newState.currentFace = action.world.faces[action.world.home_face_id];
			newState.currentMajorTri = null;
			return newState;
			
		case SELECT_FACE:
			newState.currentFace = newState.world.faces[action.id];
			newState.currentMajorTri = null;
			return newState;
			
		case SELECT_MAJORTRI:
			//newState.currentMajorTri = findMajorTri(Object.values(newState.world.faces),action.id);
			newState.currentMajorTri = newState.world.majortris[action.id];
			return newState;
			
		case SELECT_MINORTRI:
			newState.currentMinorTri = action.id;
			return newState;
		
		default:
            return state;
	}
}
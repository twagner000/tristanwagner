const initialState = {
	map: null,
	isFetchingMap: false,
};


export default function mapface(state=initialState, action) {
	let newState = Object.assign({},state);
	switch (action.type) {
		
		case 'FETCH_GAMES':
			newState.gameList = action.gameList;
			newState.gameListLoaded = true;
			return newState;
			
		case 'FETCH_MAPFACE_REQUEST':
			newState.isFetchingMap = true;
			return newState;
			
		case 'FETCH_MAPFACE_SUCCESS':
			newState.map = action.map;
			newState.isFetchingMap = false;
			return newState;
		
		default:
            return state;
	}
}
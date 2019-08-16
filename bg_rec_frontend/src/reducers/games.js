const initialState = {
	gameList: [],
	gameListLoaded: false,
	game: null,
	gameLoaded: false,
};


export default function games(state=initialState, action) {
	let newState = Object.assign({},state);
	switch (action.type) {
		
		case 'FETCH_GAMES':
			newState.gameList = action.gameList;
			newState.gameListLoaded = true;
			return newState;
			
		case 'REFRESH_GAME':
			newState.gameLoaded = false;
			return newState;
			
		case 'FETCH_GAME':
			newState.game = action.game;
			newState.gameLoaded = true;
			return newState;
		
		default:
            return state;
	}
}
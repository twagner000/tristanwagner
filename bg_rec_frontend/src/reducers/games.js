const initialState = {
	gameList: [],
	gameListLoaded: false,
	game: null,
	isFetchingGame: false,
};


export default function games(state=initialState, action) {
	let newState = Object.assign({},state);
	switch (action.type) {
		
		case 'FETCH_GAMES':
			newState.gameList = action.gameList;
			newState.gameListLoaded = true;
			return newState;
			
		case 'FETCH_GAME_REQUEST':
			newState.isFetchingGame = true;
			return newState;
			
		case 'FETCH_GAME_SUCCESS':
			newState.game = action.game;
			newState.isFetchingGame = false;
			return newState;
		
		default:
            return state;
	}
}
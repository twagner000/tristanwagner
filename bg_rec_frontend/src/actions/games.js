export const fetchGames = () => {
    return dispatch => {
        let headers = {"Content-Type": "application/json"};
        return fetch("/bg_rec/api/game/", {headers, })
            .then(res => res.json())
            .then(gameList => {
                return dispatch({
                    type: 'FETCH_GAMES',
                    gameList
                })
            })
    }
}

export const startGameRefresh = () => {
	return {type: 'REFRESH_GAME'};
}

export const fetchGame = (id) => {
    return dispatch => {
        let headers = {"Content-Type": "application/json"};
        return fetch(`/bg_rec/api/game/${id}`, {headers, })
            .then(res => res.json())
            .then(game => {
                return dispatch({
                    type: 'FETCH_GAME',
                    game
                })
            })
    }
}
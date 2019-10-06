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

export const startMapFaceRefresh = () => {
	return {type: 'FETCH_MAPFACE_REQUEST'};
}

export const fetchMapFace = (world, ring, index) => {
    return dispatch => {
        let headers = {"Content-Type": "application/json"};
        return fetch(`/triworld/api/world/${world}/face/${ring}/${index}`, {headers, })
            .then(res => res.json())
            .then(map => {
                return dispatch({
                    type: 'FETCH_MAPFACE_SUCCESS',
                    map
                })
            })
    }
}
import { combineReducers } from 'redux';
import games from "./games";


const bgRecApp = combineReducers({
  games,
})

export default bgRecApp;
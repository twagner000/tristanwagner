import React from 'react';
import {Link} from 'react-router-dom';
import {Form, Icon} from 'react-bulma-components';
import {connect} from 'react-redux';

import {games} from "../actions";


class Search extends React.Component {
	state = {game: "", game_id: null, };
	
	componentDidMount() {
        this.props.fetchGames();
    }
	
	handleChange = (event) => {
		const search_lower_case = event.target.value.toLowerCase();
		let game_id = null;
		for (let g of this.props.gameList) {
			if (g.name.toLowerCase() === search_lower_case) {
				game_id = g.objectid;
				break;
			}
		}
		this.setState({game: event.target.value, game_id: game_id});
	}
	
	render() {
		return (
			<React.Fragment>
				<Form.Field kind="addons">
					<Form.Control iconLeft fullwidth>
						<Form.Input placeholder="Select a game..." list="game_list" value={this.state.game} onChange={this.handleChange} />
						<Icon align="left"><i className={this.state.game_id == null ? "fas fa-exclamation-triangle" : "fas fa-check"}></i></Icon>
						<datalist id="game_list">
							{this.props.gameList.map((game) => (<option key={game.objectid} value={game.name}/>))}
						</datalist>
					</Form.Control>
					<Form.Control>
						<Link to={`/game/${this.state.game_id}/`} onClick={() => this.setState({game: "", game_id: null})} className="button is-primary" disabled={this.state.game_id == null ? true : false}><Icon><i className="fas fa-search"></i></Icon></Link>
					</Form.Control>
				</Form.Field>
				<Form.Field><Form.Help color="danger">{this.state.game_id == null ? "Please enter a valid game name." : ""}</Form.Help></Form.Field>
			</React.Fragment>
		)
	}
}

const mapStateToProps = state => {
	return {
		gameList: state.games.gameList,
		gameListLoaded: state.games.gameListLoaded,
	}
}

const mapDispatchToProps = dispatch => {
	return {
        fetchGames: () => {
            dispatch(games.fetchGames());
        },
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Search);
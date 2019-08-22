import React from 'react';
import {Link} from 'react-router-dom';
import {Content, Icon, Media, Level, Table} from 'react-bulma-components';
import {connect} from 'react-redux';

import {games} from "../actions";


class Game extends React.Component {
	static players(game) {
		return (game.minplayers && game.maxplayers && game.minplayers !== game.maxplayers)
			? `${game.minplayers}-${game.maxplayers}`
			: `${game.minplayers}`;
	}
	
	static playtime(game) {
		return (game.minplaytime && game.maxplaytime && game.minplaytime !== game.maxplaytime)
			? `${game.minplaytime}-${game.maxplaytime}`
			: `${game.playingtime}`;
	}
	
	render() {
		let game = this.props.game;
		let distance = this.props.distance;
		return (
			<tr>
				{distance
					? (<td><Link to={`/game/${game.objectid}/`}>{game.name}</Link></td>)
					: (<td>{game.name}</td>)}
				<td>{distance ? distance.toFixed(2) : "NA"}</td>
				<td>{game.bayesaverage.toFixed(2)}</td>
				<td>{Game.players(game)}</td>
				<td>{Game.playtime(game)}</td>
				<td><a href={`https://boardgamegeek.com/boardgame/${game.objectid}`}><Icon><i className="fas fa-external-link-alt"></i></Icon></a></td>
			</tr>
		);
	}
}


class Results extends React.Component {
	table_headers = [
		{icon: "fas fa-arrows-alt-h", description: "Distance (smaller number indicates greater similarity)"},
		{icon: "fas fa-star", description: "BGG average rating, adjusted for number of ratings"},
		{icon: "fas fa-users", description: "Players"},
		{icon: "fas fa-clock", description: "Playing time (minutes)"},
		{icon: "fas fa-external-link-alt", description: "Link to the game's BGG page"}
		];
		
	
	checkForUpdate = () => {
		if (!this.props.isFetchingGame && (this.props.game == null || parseInt(this.props.match.params.id) !== this.props.game.objectid)) {
			this.props.loadGame(this.props.match.params.id);
		}
	}
		
	componentDidMount() {
        this.checkForUpdate();
    }
	
	componentDidUpdate() {
		this.checkForUpdate();
    }
		
	render() {
		let game = this.props.game;
		if (!game) {
			return "";
		} else {
			return (
				<Content>
					<Link to="/" className="is-pulled-right delete"></Link>
					<h4>Results: {game.name}</h4>
					
					<Level breakpoint="mobile">
						<Level.Item key={game.objectid}>
							<img className="image is-96x96 has-background-dark" alt={game.name} title={game.name} src={game.thumbnail} style={{objectFit: "contain"}}/>
						</Level.Item>
					{game.gameneighbor_set.slice(0,8).map((game_neighbor, i) => (
						<Level.Item className={"" + (i>1 ? " is-hidden-mobile" : "") + (i>4 ? " is-hidden-touch" : "")} key={game_neighbor.neighbor.objectid}>
							<Link to={`/game/${game_neighbor.neighbor.objectid}/`}><img className="image is-96x96 has-background-dark" alt={game_neighbor.neighbor.name} title={game_neighbor.neighbor.name} src={game_neighbor.neighbor.thumbnail} style={{objectFit: "contain"}}/></Link>
						</Level.Item>
					))}
					</Level>
					<small>
						<Table>
							<thead>
								<tr>
									<th>Game</th>
								{this.table_headers.map(({icon, description}, i) => (
									<th key={i} title={description}><Icon><i className={icon}></i></Icon></th>
								))}
								</tr>
							</thead>
							<tbody>
								<Game game={game} key={game.objectid} />
								{game.gameneighbor_set.map((game_neighbor) => (
								<Game game={game_neighbor.neighbor} distance={game_neighbor.distance} key={game_neighbor.neighbor.objectid} />
								))}
							</tbody>
						</Table>
					</small>
					
					<p>&nbsp;</p>
					<h4>Columns Explained</h4>
					{this.table_headers.map(({icon, description}, i) => (
					<Media key={i}><Media.Item position="left"><Icon><i className={icon}></i></Icon></Media.Item><Media.Item>{description}</Media.Item></Media>
					))}
				</Content>
			);
		}
	}
}

const mapStateToProps = state => {
	return {
		game: state.games.game,
		isFetchingGame: state.games.isFetchingGame,
	}
}

const mapDispatchToProps = dispatch => {
	return {
        loadGame: (id) => {
			dispatch(games.startGameRefresh());
            dispatch(games.fetchGame(id));
        },
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Results);
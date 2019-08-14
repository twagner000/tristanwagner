import React from 'react';
import './App.css';


import 'react-bulma-components/dist/react-bulma-components.min.css';
import { Section, Container, Heading, Form, Icon, Content, Level, Table, Modal, Box, Media} from 'react-bulma-components';
import { BrowserRouter as Router, Route, Link, Switch } from "react-router-dom";
import axios from 'axios';

const BASE_URL = '/bg_rec';

function Info(props) {
	return (<p className="content">Choose a game to get recommendations of similar games.</p>);
}

class Search extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			game_list: [],
			loaded: false,
			game: "",
			game_id: null
		};
		
		this.handleChange = this.handleChange.bind(this);
	}
	
	componentDidMount() {
        axios.get(`${BASE_URL}/api/game/`)
			.then(response => this.setState({game_list: response.data, loaded: true}));
	}
	
	handleChange(event) {
		const search_lower_case = event.target.value.toLowerCase();
		let game_id = null;
		for (let g of this.state.game_list) {
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
							{this.state.game_list.map((game) => (<option key={game.objectid} value={game.name}/>))}
						</datalist>
					</Form.Control>
					<Form.Control>
						<Link to={`/game/${this.state.game_id}/`} className="button is-primary" disabled={this.state.game_id == null ? true : false}><Icon><i className="fas fa-search"></i></Icon></Link>
					</Form.Control>
				</Form.Field>
				<Form.Field><Form.Help color="danger">{this.state.game_id == null ? "Please enter a valid game name." : ""}</Form.Help></Form.Field>
			</React.Fragment>
		);
	}
}

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
	state = {game: null, loaded: false, show_info: false};
	table_headers = [
		{icon: "fas fa-arrows-alt-h", description: "Distance (smaller number indicates greater similarity)"},
		{icon: "fas fa-star", description: "BGG average rating, adjusted for number of ratings"},
		{icon: "fas fa-users", description: "Players"},
		{icon: "fas fa-clock", description: "Playing time (minutes)"},
		{icon: "fas fa-external-link-alt", description: "Link to the game's BGG page"}
		];
	
	getResults() {
		axios.get(`${BASE_URL}/api/game/${this.props.match.params.id}/`)
			.then(response => this.setState({game: response.data, loaded: true}));
	}
	
	componentDidMount() {
		this.getResults();
	}
	
	componentDidUpdate() {
		if (this.state.loaded === true) {
			if (parseInt(this.props.match.params.id) !== this.state.game.objectid) {
				this.setState({loaded: false});
				this.getResults();
			}
		}
	}
	
	render() {
		let game = this.state.game;
		if (!game) {
			return "";
		} else {
			return (
				<Content>
					<button className="is-pulled-right button is-white has-text-link" onClick={() => this.setState({show_info: this.state.show_info ? false : true})}><Icon><i className="fas fa-question-circle"></i></Icon></button>
					<h4>Results: {game.name}</h4>
					
					<Modal show={this.state.show_info} onClose={() => this.setState({show_info: false})} closeOnBlur showClose>
						<Modal.Content>
							<Box>
								<Content>
									<h4>Columns Explained</h4>
									{this.table_headers.map(({icon, description}, i) => (
									<Media key={i}><Media.Item position="left"><Icon><i className={icon}></i></Icon></Media.Item><Media.Item>{description}</Media.Item></Media>
									))}
								</Content>
							</Box>
						</Modal.Content>
					</Modal>
					
					<Level breakpoint="mobile">
					{game.gameneighbor_set.slice(0,9).map((game_neighbor, i) => (
						<Level.Item className={"" + (i>2 ? " is-hidden-mobile" : "") + (i>5 ? " is-hidden-touch" : "")} key={game_neighbor.neighbor.objectid}>
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
				</Content>
			);
		}
	}
}

class App extends React.Component {
	render() {
		return (
			<Router basename={BASE_URL}>
				<Section>
					<Container>
						<Heading>Board Game Recommender</Heading>
						<Search />
						<Switch>
							<Route path="/game/:id" component={Results} />
							<Route exact path="/" component={Info} />
						</Switch>
					</Container>
				</Section>
			</Router>
		);
	}
}

export default App;

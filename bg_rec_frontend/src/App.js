import React from 'react';
import './App.css';


import 'react-bulma-components/dist/react-bulma-components.min.css';
import { Section, Container, Heading, Form, Icon, Content, Level, Table} from 'react-bulma-components';
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
	state = {game: null, loaded: false};
	
	getResults() {
		console.log("calling getResults");
		if (this.state.game == null || this.props.match.params.id !== this.state.game.objectid) {
			console.log(this.props.match.params.id);
			//console.log(this.state.game.objectid);
			axios.get(`${BASE_URL}/api/game/${this.props.match.params.id}/`)
				.then(response => this.setState({game: response.data, loaded: true}));
		}
	}
	
	componentDidMount() {
		this.getResults();
	}
	
	componentDidUpdate() {
		this.getResults();
	}
	
	render() {
		let game = this.state.game;
		if (!game) {
			return "";
		} else {
			return (
				<Content>
					<h4>Results: {game.name}</h4>
					
					<Level breakpoint="mobile">
					{game.gameneighbor_set.slice(0,9).map((game_neighbor, i) => (
						<Level.Item className={"" + (i>2 ? " is-hidden-mobile" : "") + (i>5 ? " is-hidden-touch" : "")} key={game_neighbor.neighbor.objectid}>
							<Link to={`/game/${game_neighbor.neighbor.objectid}/`}><img className="image is-96x96 has-background-dark" alt={game_neighbor.neighbor.name} title={game_neighbor.neighbor.name} src={game_neighbor.neighbor.thumbnail} style={{objectFit: "contain"}}/></Link>
						</Level.Item>
					))}
					</Level>
					<Table>
						<thead>
							<tr>
								<th>Game</th>
								<th><Icon><i className="fas fa-arrows-alt-h"></i></Icon></th>
								<th><Icon><i className="fas fa-star"></i></Icon></th>
								<th><Icon><i className="fas fa-users"></i></Icon></th>
								<th><Icon><i className="fas fa-clock"></i></Icon></th>
								<th></th>
							</tr>
						</thead>
						<tbody>
							<Game game={game} key={game.objectid} />
							{game.gameneighbor_set.map((game_neighbor) => (
							<Game game={game_neighbor.neighbor} distance={game_neighbor.distance} key={game_neighbor.neighbor.objectid} />
							))}
						</tbody>
					</Table>
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
							<Route exact path="/" component={Info} />
							<Route path="/game/:id" component={Results} />
						</Switch>
					</Container>
				</Section>
			</Router>
		);
	}
}

export default App;

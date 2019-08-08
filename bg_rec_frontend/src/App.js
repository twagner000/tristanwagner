import React from 'react';
import './App.css';


import 'react-bulma-components/dist/react-bulma-components.min.css';
import { Section, Container, Heading, Form, Icon, Columns, Box, Content, Level, Card, Image} from 'react-bulma-components';
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
		let neigh = this.props.game_neighbor;
		return (
			<Card>
				<Card.Content>
					{this.props.show_image
						? (<p className="has-text-centered"><img src={neigh.neighbor.thumbnail} /></p>)
						: ""}
					<h4><Link to={`/game/${neigh.neighbor.objectid}/`}>{neigh.neighbor.name}</Link></h4>
					<Columns gapless>
						<Columns.Column size="one-third">
							<Icon><i className="fas fa-arrows-alt-h"></i></Icon>{neigh.distance.toFixed(3)}
						</Columns.Column>
						<Columns.Column size="one-third">
							<Icon><i className="fas fa-globe"></i></Icon>{neigh.neighbor.usersrated}
						</Columns.Column>
						<Columns.Column size="one-third">
							<a href={`https://boardgamegeek.com/boardgame/${neigh.neighbor.objectid}`}><Icon><i className="fas fa-external-link-alt"></i></Icon> BGG</a>
						</Columns.Column>
						
						<Columns.Column size="one-third">
							<Icon><i className="fas fa-users"></i></Icon>{Game.players(neigh.neighbor)}
						</Columns.Column>
						<Columns.Column size="one-third">
							<Icon><i className="fas fa-clock"></i></Icon>{Game.playtime(neigh.neighbor)}
						</Columns.Column>
						<Columns.Column size="one-third">
							<Icon><i className="fas fa-star"></i></Icon>{neigh.neighbor.bayesaverage.toFixed(2)}
						</Columns.Column>
					</Columns>
				</Card.Content>
			</Card>
		);
	}
}

class Results extends React.Component {
	state = {game: null, loaded: false};
	
	getResults() {
        axios.get(`${BASE_URL}/api/game/${this.props.match.params.id}/`)
			.then(response => this.setState({game: response.data, loaded: true}));
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
					<Columns gapless>
						<Columns.Column size="two-thirds"><h4>Results: {game.name}</h4></Columns.Column>
						<Columns.Column>
						<Level breakpoint="mobile" className="is-marginless">
								<Level.Item><a className="tooltip" data-tooltip={`Adjusted average of ${game.usersrated} ratings`}><Icon><i className="fas fa-star"></i></Icon>{game.bayesaverage.toFixed(2)}</a></Level.Item>
								<Level.Item><Icon><i className="fas fa-users"></i></Icon>{Game.players(game)}</Level.Item>
								<Level.Item><Icon><i className="fas fa-clock"></i></Icon>{Game.playtime(game)}</Level.Item>
								<Level.Item><a href={`https://boardgamegeek.com/boardgame/${game.objectid}`}><Icon><i className="fas fa-external-link-alt"></i></Icon></a></Level.Item>
						</Level>
						</Columns.Column>
					</Columns>
					
					<Columns multiline>
					{game.gameneighbor_set.slice(0,3).map((game_neighbor) => (
						<Columns.Column size="one-third" key={game_neighbor.neighbor.objectid}><Game show_image game_neighbor={game_neighbor} /></Columns.Column>
					))}{game.gameneighbor_set.slice(3).map((game_neighbor) => (
						<Columns.Column size="one-third" key={game_neighbor.neighbor.objectid}><Game game_neighbor={game_neighbor} /></Columns.Column>
					))}
					</Columns>
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

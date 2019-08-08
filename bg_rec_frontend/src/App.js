import React from 'react';
import './App.css';

import 'react-bulma-components/dist/react-bulma-components.min.css';
import { Section, Container, Heading, Form, Icon} from 'react-bulma-components';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import axios from 'axios';

const BASE_URL = '/bg_rec';

export class Info extends React.Component {
	render() {
		return (<p className="content">Choose a game to get recommendations of similar games.</p>);
	}
}

export class Search extends React.Component {
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
						<Link to={`${this.state.game_id}/`} className="button is-primary" disabled={this.state.game_id == null ? true : false}><Icon><i className="fas fa-search"></i></Icon></Link>
					</Form.Control>
				</Form.Field>
				<Form.Field><Form.Help color="danger">{this.state.game_id == null ? "Please enter a valid game name." : ""}</Form.Help></Form.Field>
			</React.Fragment>
		);
	}
}

export class Results extends React.Component {
	state = {game: null, loaded: false};
	
	componentDidMount() {
        axios.get(`${BASE_URL}/api/game/${this.props.match.params.id}/`)
			.then(response => this.setState({game: response.data, loaded: true}));
	}
	
	render() {
		let game = this.state.game;
		if (!game) {
			return "";
		} else {
			return (
				<div className="content">
					<h4>Results for {game.name}:</h4>
					<ul>
					{game.gameneighbor_set.map((neigh) => (
						<li key={neigh.neighbor.objectid}>{neigh.distance}: {neigh.neighbor.name}</li>
					))}
					</ul>
				</div>
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
						<Route exact path="/" component={Info} />
						<Route path="/:id" component={Results} />
					</Container>
				</Section>
			</Router>
		);
	}
}

export default App;

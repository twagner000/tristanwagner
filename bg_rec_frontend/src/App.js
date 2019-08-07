import React from 'react';
import './App.css';

import 'react-bulma-components/dist/react-bulma-components.min.css';
import { Section, Container, Heading, Button, Form, Icon} from 'react-bulma-components';
import BGRecommenderService from "./BGRecommenderService";

export class RecommendationSearch extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			game: "",
			game_id: null
		};
		
		this.handleChange = this.handleChange.bind(this);
	}
	
	handleChange(event) {
		const search_lower_case = event.target.value.toLowerCase();
		let game_id = null;
		for (let g of this.props.game_list) {
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
							{this.props.game_list.map((game) => (<option key={game.objectid} value={game.name}/>))}
						</datalist>
					</Form.Control>
					<Form.Control>
						<Button onClick={() => this.props.onSearch(this.state.game_id)} color="primary" disabled={this.state.game_id == null ? true : false}><Icon><i className="fas fa-search"></i></Icon></Button>
					</Form.Control>
				</Form.Field>
				<Form.Field><Form.Help color="danger">{this.state.game_id == null ? "Please enter a valid game name." : ""}</Form.Help></Form.Field>
				<p className="content">Choose a game to get recommendations of similar games.</p>
			</React.Fragment>
		);
	}
}

export class RecommendationList extends React.Component {
	render() {
		let game = this.props.game;
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
	constructor(props) {
		super(props);
		this.state = {
			service: new BGRecommenderService(),
			game_list: [],
			loaded: false,
			game: null
		};
		
		this.handleSearch = this.handleSearch.bind(this);
	}
	
	componentDidMount() {
		this.state.service.getGameList()
			.then(data => this.setState({ game_list: data, loaded: true }));
	}
	
	handleSearch(game_id) {
		console.log(game_id);
		this.state.service.getGameDetail(game_id)
			.then(data => this.setState({ game: data }));
	}
	
	render() {
		return (
			<Section>
				<Container>
					<Heading>Board Game Recommender</Heading>
					{ this.state.loaded ? (
						<React.Fragment>
							<RecommendationSearch game_list={this.state.game_list} onSearch={this.handleSearch} />
							<RecommendationList game={this.state.game} />
						</React.Fragment>
					) : (
						<p>Loading game list...</p>
					)}
				</Container>
			</Section>
		);
	}
}

export default App;

import React from 'react';
import './App.css';

import 'react-bulma-components/dist/react-bulma-components.min.css';
import {Section, Container, Heading, Button, Form, Icon} from 'react-bulma-components';
//import Select from 'react-select'; //, { createFilter }

import BGRecommenderService from "./BGRecommenderService";

class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			service: new BGRecommenderService(),
			game_list: [],
			game: "",
			game_id: null
		};
		this.handleChange = this.handleChange.bind(this);
	}
		
		
	componentDidMount() {
		this.state.service.getGameList()
			.then(data => this.setState({ game_list: data }));
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
			<Section>
				<Container>
					<Heading>Board Game Recommender</Heading>
					<p className="content">Choose a game to get recommendations of similar games.</p>
					<Form.Field kind="addons">
						<Form.Control iconLeft fullwidth>
							<Form.Input placeholder="Select a game..." list="game_list" value={this.state.game} onChange={this.handleChange} />
							<Icon align="left"><i className={this.state.game_id == null ? "fas fa-exclamation-triangle" : "fas fa-check"}></i></Icon>
							<datalist id="game_list">
								{this.state.game_list.map((game) => (<option key={game.objectid} value={game.name}/>))}
							</datalist>
						</Form.Control>
						<Form.Control>
							<Button color="primary" disabled={this.state.game_id == null ? true : false}><Icon><i className="fas fa-search"></i></Icon></Button>
						</Form.Control>
					</Form.Field>
					<Form.Help color="danger">{this.state.game_id == null ? "Please enter the name of a valid game." : ""}</Form.Help>
					
					<p className="content">{this.state.game_id}</p>
				</Container>
			</Section>
		);
	}
	//filterOption={createFilter({ignoreCase: true, ignoreAccents: true, trim: false, matchFrom: 'start'})}
	
	/*						<Form.Control>
							<Form.Select>
								<option></option>
								{this.state.game_list.map((game) => (<option value="{game.objectid}">{game.name}</option>))}
							</Form.Select>
							
							
						</Form.Control>*/
}

export default App;

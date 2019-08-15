import React from 'react';
import {Route, Switch, BrowserRouter} from 'react-router-dom';
import {Section, Container, Heading} from 'react-bulma-components';

import Search from "./components/Search";
import Home from "./components/Home";
import Results from "./components/Results";

const BASE_URL = '/bg_rec';

class App extends React.Component {
	render() {
		return (
			<Section>
				<Container>
					<BrowserRouter basename={BASE_URL}>
						<Heading>Board Game Recommender</Heading>
						<Search />
						<Switch>
							<Route exact path="/game/:id" component={Results} />
							<Route component={Home} />
						</Switch>
					</BrowserRouter>
				</Container>
			</Section>
		);
	}
}

export default App;
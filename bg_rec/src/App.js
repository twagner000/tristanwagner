import React from 'react';
import { Route, Switch, BrowserRouter } from 'react-router-dom';
import { Section, Container, Heading } from 'react-bulma-components';
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";

import bgRecApp from "./reducers";

import Search from "./components/Search";
import Home from "./components/Home";
import Results from "./components/Results";

let store = createStore(bgRecApp, applyMiddleware(thunk));

const BASE_URL = '/bg_rec';

class App extends React.Component {
	render() {
		return (
			<Section>
				<Container>
					<Provider store={store}>
						<BrowserRouter basename={BASE_URL}>
							<Heading>Board Game Recommender</Heading>
							<Search />
							<Switch>
								<Route exact path="/game/:id" component={Results} />
								<Route component={Home} />
							</Switch>
						</BrowserRouter>
					</Provider>
				</Container>
			</Section>
		);
	}
}

export default App;
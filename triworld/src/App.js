import React from 'react';
import { Route, Switch, BrowserRouter } from 'react-router-dom';
import { Section, Container, Title } from "rbx";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";

import bgRecApp from "./reducers";

//import Search from "./components/Search";
import Home from "./components/Home";
import MapFace from "./components/MapFace";

let store = createStore(bgRecApp, applyMiddleware(thunk));

const BASE_URL = '/triworld';

class App extends React.Component {
	render() {
		return (
			<Section>
				<Container>
					<Provider store={store}>
						<BrowserRouter basename={BASE_URL}>
							<Title>TriWorld</Title>
							<p>nav</p>
							<Switch>
								<Route exact path="/map/f/:ring-:index" component={MapFace} />
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
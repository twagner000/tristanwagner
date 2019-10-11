import React from 'react';
import { Route, Switch, BrowserRouter, Link } from 'react-router-dom';
import { Section, Container, Title, Level, Icon, Button } from "rbx";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";

import triWorldApp from "./reducers";

import TriWorldNav from "./components/TriWorldNav";
import Home from "./components/Home";
import LoadWorld from "./components/LoadWorld";
import MapFace from "./components/MapFace";

let store = createStore(triWorldApp, applyMiddleware(thunk));

const BASE_URL = '/triworld';


class App extends React.Component {
	render() {
		return (
			<Section>
				<Container>
					<Provider store={store}>
						<BrowserRouter basename={BASE_URL}>
							<TriWorldNav />
							<Switch>
								<Route exact path="/world/:world_id" component={LoadWorld} />
								<Route exact path="/map/face" component={MapFace} />
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
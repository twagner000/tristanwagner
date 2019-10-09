import React from 'react';
import { Route, Switch, BrowserRouter, Link } from 'react-router-dom';
import { Section, Container, Title, Level, Icon, Button } from "rbx";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";

import triWorldApp from "./reducers";

//import Search from "./components/Search";
import TriWorldNav from "./components/TriWorldNav";
import Home from "./components/Home";
import MapFace from "./components/MapFace";

let store = createStore(triWorldApp, applyMiddleware(thunk));

const BASE_URL = '/triworld';

//<Level.Item><Icon><i className="fas fa-caret-square-down"></i></Icon></Level.Item>

class App extends React.Component {
	render() {
		return (
			<Section>
				<Container>
					<Provider store={store}>
						<BrowserRouter basename={BASE_URL}>
							<TriWorldNav />
							<Switch>
								<Route exact path="/map/f/:face_id" component={MapFace} />
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
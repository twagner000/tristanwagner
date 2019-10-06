import React from 'react';
import { Route, Switch, BrowserRouter, Link } from 'react-router-dom';
import { Section, Container, Title, Level, Icon } from "rbx";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";

import triWorldApp from "./reducers";

//import Search from "./components/Search";
import Home from "./components/Home";
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
							<Title><Icon><i className="fas fa-hiking"></i></Icon> TriWorld</Title>
							<Level>
								<Level.Item align="left"><Link to="/w/12/map/f/0-0">0-0</Link></Level.Item>
								<Level.Item align="left"><Link to="/w/12/map/f/1-0">1-0</Link></Level.Item>
								<Level.Item align="left"><Link to="/w/12/map/f/2-0">2-0</Link></Level.Item>
								<Level.Item align="left"><Link to="/w/12/map/f/3-0">3-0</Link></Level.Item>
							</Level>
							<Switch>
								<Route exact path="/w/:world/map/f/:ring-:index" component={MapFace} />
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
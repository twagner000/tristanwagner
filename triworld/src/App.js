import React from 'react';
import { Route, Switch, BrowserRouter, Link } from 'react-router-dom';
import { Section, Container, Title, Level, Icon, Button } from "rbx";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";

import triWorldApp from "./reducers";

//import Search from "./components/Search";
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
							<Level>
								<Level.Item><Button as={Link} to="/"><Icon><i className="fas fa-hiking"></i></Icon><span>TriWorld</span></Button></Level.Item>
								<Level.Item>
									<Button.Group hasAddons>
										<Button as={Link} to="/" state="active"><Icon><i className="fas fa-search-minus"></i></Icon></Button>
										<Button as={Link} to="/" disabled><Icon><i className="fas fa-search-plus"></i></Icon></Button>
										<Button as={Link} to="/" disabled><Icon><i className="fas fa-gem"></i></Icon></Button>
									</Button.Group>
								</Level.Item>
							</Level>
							<Switch>
								<Route exact path="/w/:world_id/map/f/:face_id" component={MapFace} />
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
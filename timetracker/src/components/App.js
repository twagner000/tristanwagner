import React from "react";
import Form from "./Form";
import { RecentEntryList, UpdateEntryForm } from "./Entry";
import TimeTrackerService, {ServiceContext} from "./TimeTrackerService";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";


class App extends React.Component {
	state = {
			loaded: false,
			service: null
		};
		
	constructor(props) {
		super(props);
		const service = new TimeTrackerService();
		service.getToken().then(() => this.setState({ loaded: true, service: service}))
	}
	
	render() {
		if (!this.state.loaded)
			return (<p>Authenticating...</p>);
		return (
			<Router basename="/timetracker">
				<ServiceContext.Provider value={this.state.service}>
					<nav>
						<ul>
							<li><Link to="/">Recent</Link></li>
							<li><Link to="/entry">Start</Link></li>
						</ul>
					</nav>
					<Route exact path="/" component={RecentEntryList} />
					<Route exact path="/entry" render={props => <Form {...props} endpoint="api/entry/" token={this.state.token} />} />
					<Route path="/entry/:id" component={UpdateEntryForm} />
				</ServiceContext.Provider>
			</Router>
		);
	}
}

export default App;
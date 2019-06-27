import React from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import './App.css';
import { EntryRecentList, EntryCreateUpdateForm } from "./Entry";
import { TimePeriodSearch, TimePeriodSummary } from "./TimePeriod";
import TimeTrackerService, {ServiceContext} from "./TimeTrackerService";

class Home extends React.Component {
	static contextType = ServiceContext;
	
	render() {
		return (
			<React.Fragment>
				<EntryRecentList />
				<Link to="period/" className="btn btn-outline-primary">Time Period Summary</Link>
			</React.Fragment>
		);
	}
}

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
					<Switch>
						<Route exact path="/" component={Home} />
						<Route exact path="/period/" component={TimePeriodSummary} />
						<Route exact path="/entry/" component={EntryCreateUpdateForm} />
						<Route path="/entry/:id" component={EntryCreateUpdateForm} />
						<Route render={() => <p>Not Found</p>} />
					</Switch>
				</ServiceContext.Provider>
			</Router>
			
		);
	}
}

export default App;
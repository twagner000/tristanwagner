import React from "react";
import Form from "./Form";
import { EntryRecentList, EntryCreateUpdateForm } from "./Entry";
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
					<Route exact path="/" component={EntryRecentList} />
					<Route path="/entry/:id" component={EntryCreateUpdateForm} />
					<Route exact path="/entry/" component={EntryCreateUpdateForm} />
				</ServiceContext.Provider>
			</Router>
		);
	}
}

export default App;
import React from "react";
import Form from "./Form";
import { RecentEntryList, UpdateEntryForm } from "./Entry";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";


class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			placeholder: 'Authenticating...',
			token: null
		};
		
		fetch("/accounts/auth-token")
			.then(response => {
				if (response.status !== 200) {
					return this.setState({ placeholder: "You must be logged into use the Time Tracker app." });
				}
				return response.json();
			})
			.then(data => this.setState({ token: data.token, placeholder: "Token established." }));
		
	}
	
	render() {
		if (this.state.token == null)
			return (<p>{this.state.placeholder}</p>);
		return (
			<Router basename="/timetracker">
				<nav>
					<ul>
						<li><Link to="/">Recent</Link></li>
						<li><Link to="/entry">Start</Link></li>
					</ul>
				</nav>
				<Route exact path="/" render={props => <RecentEntryList {...props} token={this.state.token} />} />
				<Route exact path="/entry" render={props => <Form {...props} endpoint="api/entry/" token={this.state.token} />} />
				<Route path="/entry/:id" render={props => <UpdateEntryForm {...props} token={this.state.token} />} />
			</Router>
		);
		//<div className="App">
		/*<!--DataProvider endpoint="api/recent-entry/" token={this.state.token} render={data => <Table data={data} />} /-->*/
	}
}

export default App;
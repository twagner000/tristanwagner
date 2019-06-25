import React, {Component} from "react";
import DataProvider from "./DataProvider";
import Table from "./Table";
import Form from "./Form";
import RecentEntries from "./RecentEntries";


class App extends Component {
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
			<div className="App">
				<RecentEntries endpoint="api/entry/recent/" token={this.state.token} />
				<Form endpoint="api/entry/" />
			</div>
		);
		/*<!--DataProvider endpoint="api/recent-entry/" token={this.state.token} render={data => <Table data={data} />} /-->*/
	}
}

export default App;
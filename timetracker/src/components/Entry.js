import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";
import { format } from 'date-fns';
import { Link } from "react-router-dom";

const endpoint_base = '/timetracker/api/';

class Entry extends React.Component {
	render() {
		if (this.props.data.end) {
			return (
				<React.Fragment>
					<div><Link to="entry/" className="btn btn-outline-primary"><i className="fas fa-play"></i></Link></div>
					<div><b>{this.props.data.task.full_name}</b><br/>{this.props.data.hours.toFixed(2)} hours ending {format(this.props.data.end, 'M/D/YY h:mma')}<br/><em>{this.props.data.comments}</em></div>
				</React.Fragment>
			);
		} else {
			return (
				<React.Fragment>
					<div><Link to={'entry/' + this.props.data.id} className="btn btn-outline-danger"><i className="fas fa-stop"></i></Link></div>
					<div><b>{this.props.data.task.full_name}</b><br/>Started {format(this.props.data.start, 'M/D/YY h:mma')}<br/><em>{this.props.data.comments}</em></div>
				</React.Fragment>
			);
		}
	}
}


export class RecentEntryList extends React.Component {
	static propTypes = {
		token: PropTypes.string.isRequired
	};
	
	state = {
		data: [],
		loaded: false,
		placeholder: "Loading..."
	};
	
	componentDidMount() {
		const headers = {
            'Content-Type': 'application/json',
			'Authorization': 'Token ' + this.props.token
        };

		fetch(endpoint_base+"entry/recent/", {headers})
			.then(response => {
				if (response.status !== 200) {
					return this.setState({ placeholder: "Something went wrong" });
				}
				return response.json();
			})
			.then(data => this.setState({ data: data, loaded: true }));
	}
	
	render() {
		if (!this.state.loaded) {
			return (<p>{this.state.placeholder}</p>);
		} else {
			return (
				<React.Fragment>
					<h3>Recent Entries</h3>
					<div style={{display: 'grid', gridTemplateColumns: 'auto 1fr', gridGap: '.5rem'}}>
						{this.state.data.map((entry,i) => (<Entry data={entry} key={key(entry)} />))}
					</div>
				</React.Fragment>
			);
		}
	}
}

export class UpdateEntryForm extends React.Component {
	static propTypes = {
		token: PropTypes.string.isRequired
	};
	
	state = {
		loaded: false,
		placeholder: "Loading...",
		data: []
	};
	
	componentDidMount() {
		const headers = {
            'Content-Type': 'application/json',
			'Authorization': 'Token ' + this.props.token
        };

		fetch(endpoint_base+"entry/"+this.props.match.params.id, {headers})
			.then(response => {
				if (response.status !== 200) {
					return this.setState({ placeholder: "Something went wrong" });
				}
				return response.json();
			})
			.then(data => {console.log(data); this.setState({ data: data, loaded: true })});
	}

	handleChange = e => {
		this.setState({ ["data."+e.target.name]: e.target.value });
	};

	handleSubmit = e => {
		e.preventDefault();
		const { user, task, start } = this.state;
		const entry = { user, task, start };
		const conf = {
			method: "post",
			body: JSON.stringify(entry),
			headers: new Headers({ "Content-Type": "application/json" })
		};
		fetch(this.props.endpoint, conf).then(response => console.log(response));
	};

	render() {
		return (
			<div>
				<h3>Update entry with id={this.state.data.id}</h3>
				<form onSubmit={this.handleSubmit}>
					<div className="field">
					<label className="label">User</label>
					<div className="control">
					<input
					className="input"
					type="text"
					name="user"
					onChange={this.handleChange}
					value={this.state.data.user}
					required
					/>
					</div>
					</div>
					
					<div className="field">
					<label className="label">Task</label>
					<div className="control">
					<input
					className="input"
					type="text"
					name="task"
					onChange={this.handleChange}
					value={this.state.data.task}
					required
					/>
					</div>
					</div>
					
					<div className="field">
					<label className="label">Start</label>
					<div className="control">
					<input
					className="input"
					type="datetime-local"
					name="start"
					onChange={this.handleChange}
					value={this.state.data.start}
					required
					/>
					</div>
					</div>
					
					<div className="control">
					<button type="submit" className="button is-info">
					Add entry
					</button>
					</div>
				</form>
			</div>
		);
	}
}
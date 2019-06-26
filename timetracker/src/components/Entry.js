import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";
import { format } from 'date-fns';
import { Link } from "react-router-dom";
import Select from 'react-select';

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


class TaskSelect extends React.Component {
	static propTypes = {
		token: PropTypes.string.isRequired
	};
	
	// Teach Autosuggest how to calculate suggestions for any given input value.
	getSuggestions(value) {
		const escapedValue = value.trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
		if (escapedValue === '') {
			return [];
		}
		const regex = new RegExp(escapedValue, 'i');
		return this.state.full_list.filter(item => regex.test(item.full_name));
	}
	
	constructor(props) {
		super(props);

		this.state = {
			value: '',
			suggestions: [],
			full_list: []
		};
	}
	
	componentDidMount() {
		const headers = {
            'Content-Type': 'application/json',
			'Authorization': 'Token ' + this.props.token
        };

		fetch(endpoint_base+"task/", {headers})
			.then(response => {
				if (response.status !== 200) {
					return this.setState({ placeholder: "Something went wrong" });
				}
				return response.json();
			})
			.then(data => this.setState({full_list: data}));
	}

	render() {
		const { value, suggestions } = this.state;

		// Autosuggest will pass through all these props to the input.
		const inputProps = {
			placeholder: 'Type a task',
			value,
			onChange: (event, { newValue }) => this.setState({value: newValue})
		};

		return (
			<Autosuggest
				suggestions={suggestions}
				onSuggestionsFetchRequested={({ value }) => this.setState({suggestions: this.getSuggestions(value)})}
				onSuggestionsClearRequested={() => this.setState({suggestions: []})}
				getSuggestionValue={suggestion => suggestion.id.toString()}
				renderSuggestion={suggestion => suggestion.full_name}
				inputProps={inputProps}
			/>
		);
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
		entry_loaded: false,
		placeholder: "Loading...",
		data: [],
		value: "",
		suggestions: [],
		full_list: [],
		task_options: [],
		task: undefined
	};
	
	getSuggestions(value) {
		const escapedValue = value.trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
		if (escapedValue === '') {
			return [];
		}
		const regex = new RegExp(escapedValue, 'i');
		return this.state.full_list.filter(item => regex.test(item.full_name));
	}
	
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
			.then(data => {console.log(data); this.setState({ data: data, entry_loaded: true })});
			
		fetch(endpoint_base+"task/", {headers})
			.then(response => {
				if (response.status !== 200) {
					return this.setState({ placeholder: "Something went wrong" });
				}
				return response.json();
			})
			.then(data => this.setState({full_list: data, task: data[0]}));
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
		const { value, suggestions } = this.state;

		// Autosuggest will pass through all these props to the input.
		const inputProps = {
			placeholder: 'Type a task',
			value,
			onChange: (event, { newValue }) => {
				this.setState({value: newValue});
			}
		};
		if (!this.state.entry_loaded) {
			return (<p>{this.state.placeholder}</p>);
		} else {
			return (
				<div>
					<h3>Update entry with id={this.state.data.id}</h3>
					<form onSubmit={this.handleSubmit}>
						<Select
							name="task"
							
							options={this.state.full_list}
							getOptionLabel={option => option.full_name}
							getOptionValue={option => option.id}
							onChange={(option, meta) => { this.setState({task: option}); console.log(option, meta); } }
						/>
						<p>{this.state.data.task.id} / {this.state.task ? this.state.task.id : 'na'}</p>
						
					</form>
				</div>
			);
		}
		//defaultValue={this.state.full_list.filter(option => option.id == this.state.data.task.id)}
		//onChange={option => this.setState({task_id: option.id})}
	}
	/*<div className="field">
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
					</div>*/
}
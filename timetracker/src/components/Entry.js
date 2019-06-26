import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";
import { format } from 'date-fns';
import { Link, withRouter } from "react-router-dom";
import Select from 'react-select';

const endpoint_base = '/timetracker/api/';

class Entry extends React.Component {
	render() {
		if (this.props.data.end) {
			return (
				<React.Fragment>
					<div><Link to="entry/" className="btn btn-outline-primary"><i className="fas fa-play"></i></Link></div>
					<div><b>{this.props.data.task_obj.full_name}</b><br/>{this.props.data.hours.toFixed(2)} hours ending {format(this.props.data.end, 'M/D/YY h:mma')}<br/><em>{this.props.data.comments}</em></div>
				</React.Fragment>
			);
		} else {
			return (
				<React.Fragment>
					<div><Link to={'entry/' + this.props.data.id} className="btn btn-outline-danger"><i className="fas fa-stop"></i></Link></div>
					<div><b>{this.props.data.task_obj.full_name}</b><br/>Started {format(this.props.data.start, 'M/D/YY h:mma')}<br/><em>{this.props.data.comments}</em></div>
				</React.Fragment>
			);
		}
	}
}


export class RecentEntryList extends React.Component {
	static propTypes = {
		service: PropTypes.object.isRequired
	};
	
	state = {
		data: [],
		loaded: false,
		placeholder: "Loading..."
	};
	
	componentDidMount() {
		this.props.service.getRecentEntries()
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
		service: PropTypes.object.isRequired
	};
	
	state = {
		placeholder: "Loading...",
		loaded: false,
		submitting: false,
		entry: [],
		task_list: [],
		task: [],
		start: "",
		end: "",
		comments: ""
	};
	
	constructor(props) {
		super(props);
		this.handleChange = this.handleChange.bind(this);
	}
	
	componentDidMount() {
		const p = [];
		
		p.push(this.props.service.getEntry(this.props.match.params.id)
			.then(data => this.setState({
				entry: data,
				comments: data.comments,
				start: data.start.match(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/)[0],
				end: data.end ? data.end.match(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/)[0] : ""
			})));
			
		p.push(this.props.service.getTasks()
			.then(data => this.setState({task_list: data})));
			
		Promise.all(p)
			.then(() => {
				this.setState({loaded: true, task: this.state.task_list.filter(option => option.id == this.state.entry.task)});
				console.log(this.state.entry);
			});
	}

	handleChange(event) {
		this.setState({ [event.target.name]: event.target.value });
	};

	handleSubmit = e => {
		e.preventDefault();
		this.setState({submitting: true});
		const entry = {
			'id': this.state.entry.id,
			'owner': this.state.entry.owner,
			'task': this.state.task[0].id,
			'start': this.state.start,
			'end': this.state.end,
			'comments': this.state.comments
		};
		console.log(entry);
		this.props.service.updateEntry(entry)
			.then((result) => this.props.history.push('/'))
			.catch((err) => console.log(err));
		
	};

	render() {
		if (!this.state.loaded) {
			return (<p>{this.state.placeholder}</p>);
		} else {
			return (
				<div>
					<h3>Update Entry</h3>
					<form onSubmit={this.handleSubmit}>
						<div className="form-group">
							<label>Task</label>
							<Select
								name="task"
								required
								options={this.state.task_list}
								getOptionLabel={option => option.full_name}
								getOptionValue={option => option.id}
								value={this.state.task}
								onChange={(option, meta) => this.setState({task: [option]}) }
							/>
						</div>
						<div className="form-group">
							<label>Start</label>
							<input
								className="form-control"
								type="datetime-local"
								name="start"
								required
								value={this.state.start}
								onChange={this.handleChange}
							/>
						</div>
						<div className="form-group">
							<label>End</label>
							<input
								className="form-control"
								type="datetime-local"
								name="end"
								value={this.state.end}
								onChange={this.handleChange}
							/>
							<button className="btn btn-outline-primary" type="button"><i className="fas fa-clock"></i></button>
							<button className="btn btn-outline-primary" type="button"><i className="fas fa-times"></i></button>
						</div>
						<div className="form-group">
							<label>Comments</label>
							<textarea
								className="form-control"
								name="comments"
								value={this.state.comments}
								onChange={this.handleChange}
							/>
						</div>
						<button type="submit" className="btn btn-primary" disabled={this.state.submitting}>Update</button>
					</form>
				</div>
			);
		}
	}
}
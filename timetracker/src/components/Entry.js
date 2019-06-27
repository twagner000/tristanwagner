import React from "react";
//import PropTypes from "prop-types";
import key from "weak-key";
import { format } from 'date-fns';
import { Link, withRouter } from "react-router-dom";
import Select from 'react-select';
import { ServiceContext } from "./TimeTrackerService";

const endpoint_base = '/timetracker/api/';

class Entry extends React.Component {
	render() {
		if (this.props.data.end) {
			return (
				<React.Fragment>
					<div><Link to={{ pathname: "entry/", search: "?task_id="+this.props.data.task }} className="btn btn-outline-primary"><i className="fas fa-play"></i></Link></div>
					<div>
						<h6 style={{marginBottom: ".2rem"}}>{this.props.data.task_obj.full_name}</h6>
						<div>{this.props.data.hours.toFixed(2)} hours ending {format(this.props.data.end, 'M/D/YY h:mma')}
						<br/><em>{this.props.data.comments}</em></div>
					</div>
					<div><Link to={'entry/' + this.props.data.id} className="btn btn-link"><i className="fas fa-edit"></i></Link></div>
				</React.Fragment>
			);
		} else {
			return (
				<React.Fragment>
					<div><Link to={{ pathname: "entry/" + this.props.data.id, search: "?stop=y" }} className="btn btn-outline-danger"><i className="fas fa-stop"></i></Link></div>
					<div>
						<h6 style={{marginBottom: ".2rem"}}>{this.props.data.task_obj.full_name}</h6>
						<div>Started {format(this.props.data.start, 'M/D/YY h:mma')}
						<br/><em>{this.props.data.comments}</em></div>
					</div>
					<div><Link to={'entry/' + this.props.data.id} className="btn btn-link"><i className="fas fa-edit"></i></Link></div>
				</React.Fragment>
			);
		}
	}
}


export class EntryRecentList extends React.Component {
	static contextType = ServiceContext;
	
	state = {
		data: [],
		loaded: false,
		placeholder: "Loading..."
	};
	
	componentDidMount() {
		this.context.getRecentEntries()
			.then(data => this.setState({ data: data, loaded: true }));
	}
	
	render() {
		if (!this.state.loaded) {
			return (<p>{this.state.placeholder}</p>);
		} else {
			return (
				<React.Fragment>
					<h5>Recent Entries</h5>
					<div style={{display: 'grid', gridTemplateColumns: 'auto 1fr auto', gridColumnGap: '.5rem', gridRowGap: '1rem', marginBottom: '1rem'}}>
						{this.state.data.map((entry,i) => (<Entry data={entry} key={key(entry)} />))}
						<Link style={{gridColumn: "1/-1"}} to="entry/" className="btn btn-primary">Create an Entry</Link>
					</div>
					<h5>Stats for Time Period</h5>
					<p>blah</p>
				</React.Fragment>
			);
		}
	}
}

export class EntryCreateUpdateForm extends React.Component {
	static contextType = ServiceContext;
	
	state = {
		placeholder: "Loading...",
		loaded: false,
		submitting: false,
		task_list: [],
		task: [],
		id: null,
		task_id: null,
		start: "",
		end: "",
		comments: ""
	};
	
	constructor(props) {
		super(props);
		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}
	
	componentDidMount() {
		const p = [];
		
		if(this.props.match && this.props.match.params  &&  this.props.match.params.id) {
			p.push(this.context.getEntry(this.props.match.params.id)
				.then(data => this.setState({
					id: data.id,
					task_id: data.task,
					start: data.start.slice(0, 16),
					end: data.end ? data.end.slice(0, 16) : "",
					comments: data.comments
				})));
		}
			
		p.push(this.context.getTasks()
			.then(data => this.setState({task_list: data})));
			
		Promise.all(p)
			.then(() => {
				const uparams = new URLSearchParams(location.search);
				const task_id = uparams.get('task_id');
				const stop = uparams.get('stop');
				this.setState({
					loaded: true,
					task_id: task_id != null ? task_id : this.state.task_id,
					start: !this.state.id ? this.getLocalDate() : this.state.start,
					end: stop != null && !this.state.end ? this.getLocalDate() : this.state.end,
					task: this.state.task_list.filter(option => option.id == (task_id != null ? task_id : this.state.task_id))
				});
			});
	}

	handleChange(event) {
		this.setState({ [event.target.name]: event.target.value });
	};

	handleSubmit(event) {
		this.setState({submitting: true});
		
		const { id, task_id, task, start, end, comments } = this.state;
		
		const entry = {
			'id': id,
			'task': task[0].id,
			'start': start,
			'end': end=="" ? null : end,
			'comments': comments
		};
		
		(id ? this.context.updateEntry(entry) : this.context.createEntry(entry))
			.then((result) => this.props.history.push('/'))
			.catch((err) => console.log(err));
			
		event.preventDefault();
	};
	
	getLocalDate() {
		const date = new Date();
		const dateLocal = new Date(date.getTime() - date.getTimezoneOffset()*60*1000);
		return dateLocal.toISOString().slice(0, 16);
	}

	render() {
		if (!this.state.loaded) {
			return (<p>{this.state.placeholder}</p>);
		} else {
			return (
				<div>
					<h3>{this.state.id ? "Update" : "Create"} Entry</h3>
					<form onSubmit={this.handleSubmit}>
						<div className="form-group">
							<Select
								name="task"
								aria-label="Task"
								placeholder="Select a task..."
								required
								options={this.state.task_list}
								getOptionLabel={option => option.full_name}
								getOptionValue={option => option.id}
								value={this.state.task}
								onChange={(option, meta) => this.setState({task: [option]}) }
							/>
						</div>
						<div className="form-group" style={{display: "flex"}}>
							<button className="btn" type="button"><i className="fas fa-play"></i></button>
							<input
								className="form-control"
								type="datetime-local"
								name="start"
								aria-label="Start"
								required
								value={this.state.start}
								onChange={this.handleChange}
							/>
							<button onClick={() => this.setState({start: this.getLocalDate()})} className="btn btn-link" type="button"><i className="fas fa-clock"></i></button>
						</div>
						<div className="form-group" style={{display: "flex"}}>
							<button className="btn" type="button"><i className="fas fa-stop"></i></button>
							<input
								className="form-control"
								type="datetime-local"
								name="end"
								aria-label="End"
								value={this.state.end}
								onChange={this.handleChange}
							/>
							<button onClick={() => this.setState({end: ""})} className="btn btn-link" type="button"><i className="fas fa-times"></i></button>
							<button onClick={() => this.setState({end: this.getLocalDate()})} className="btn btn-link" type="button"><i className="fas fa-clock"></i></button>
						</div>
						<div className="form-group">
							<textarea
								className="form-control"
								name="comments"
								aria-label="Comments"
								placeholder="Comments..."
								value={this.state.comments}
								onChange={this.handleChange}
							/>
						</div>
						<div className="form-group" style={{display: "flex", justifyContent: "space-between"}}>
							<Link to="/" className="btn btn-outline-primary">Cancel</Link>
							<button type="submit" className="btn btn-primary" disabled={this.state.submitting}>Save</button>
						</div>
					</form>
				</div>
			);
		}
	}
}
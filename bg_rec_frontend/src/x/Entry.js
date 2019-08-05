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
		const end = this.props.data.end;
		const pathname = end ? "entry/" : "entry/" + this.props.data.id;
		const search = end ? "?task_id="+this.props.data.task : "?stop=y";
		const iconClass = end ? "fas fa-play" : "fas fa-stop";
		const buttonClass = end ? "button is-primary is-outlined" : "button is-danger is-outlined";
		const timeMessage = end ? this.props.data.hours.toFixed(2) + " hours ending "+format(this.props.data.end, 'M/D/YY h:mma') : "Started "+format(this.props.data.start, 'M/D/YY h:mma');
		
		return (
			<article className="media">
				<div className="media-left">
					<Link to={{ pathname: pathname, search: search }} className={buttonClass}><span className="icon"><i className={iconClass}></i></span></Link>
				</div>
				<div class="media-content">
					<div class="content">
						<strong>{this.props.data.task_obj.full_name}</strong>
						<br/><small>{timeMessage}</small>
						<br/><small><em>{this.props.data.comments}</em></small>
					</div>
				</div>
				<div class="media-right">
					<Link to={'entry/' + this.props.data.id}><span className="icon has-text-primary"><i className="fas fa-edit"></i></span></Link>
				</div>
			</article>
		);
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
				<div className="content">
					<h5>Recent Entries</h5>
					{this.state.data.map((entry,i) => (<Entry data={entry} key={key(entry)} />))}
					&nbsp;<p><Link style={{gridColumn: "1/-1"}} to="entry/" className="button is-primary is-fullwidth">Create New Entry</Link></p>
				</div>
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
		confirm_delete: false,
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
	}
	
	handleDelete = () => {
		this.context.deleteEntry(this.state.id)
			.then((result) => this.props.history.push('/'))
			.catch((err) => console.log(err));
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
	}
	
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
				<div className="content">
					<Link to="/" className="delete is-pulled-right"></Link>
					<h5>{this.state.id ? "Update" : "Create"} Entry</h5>
					<form onSubmit={this.handleSubmit}>
						<div className="field has-addons">
							<div className="control is-expanded has-icons-left">
								<input
									className="input"
									type="datetime-local"
									name="start"
									aria-label="Start"
									required
									value={this.state.start}
									onChange={this.handleChange}
								/>
								<span className="icon is-left"><i className="fas fa-play"></i></span>
							</div>
							<div className="control"><button onClick={() => this.setState({start: this.getLocalDate()})} className="button" type="button"><span className="icon has-text-primary"><i className="fas fa-clock"></i></span></button></div>
						</div>
						<div className="field has-addons">
							<div className="control is-expanded has-icons-left">
								<input
									className="input"
									type="datetime-local"
									name="end"
									aria-label="End"
									value={this.state.end}
									onChange={this.handleChange}
								/>
								<span className="icon is-left"><i className="fas fa-stop"></i></span>
							</div>
							<div className="control"><button onClick={() => this.setState({end: ""})} className="button" type="button"><span className="icon has-text-primary"><i className="fas fa-times"></i></span></button></div>
							<div className="control"><button onClick={() => this.setState({end: this.getLocalDate()})} className="button" type="button"><span className="icon has-text-primary"><i className="fas fa-clock"></i></span></button></div>
						</div>
						<div className="field is-fullwidth">
							<Select
								className="control"
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
						<div className="field is-full-width">
							<textarea
								className="textarea"
								name="comments"
								aria-label="Comments"
								placeholder="Comments..."
								value={this.state.comments}
								onChange={this.handleChange}
							/>
						</div>
						<div className="level is-mobile">
							<div className="level-left">{this.state.id ? (
								<div className="level-item"><button onClick={() => this.setState({confirm_delete: true})} type="button" className="button is-danger is-outlined" aria-label="Delete"><span className="icon"><i className="fas fa-trash"></i></span></button></div>
							) : ""}
							</div>
							<div className="level-right"><div className="level-item"><button type="submit" className="button is-primary" disabled={this.state.submitting}><span className="icon"><i className="fas fa-save"></i></span></button></div></div>
						</div>
						{this.state.confirm_delete ? (
							<article className="message is-danger">
								<div className="message-header"><div><span className="icon"><i className="fas fa-exclamation-triangle"></i></span> Please Confirm</div></div>
								<div className="message-body">
									<p>Are you sure you want to delete this entry?</p>
									<div className="level is-mobile">
										<div className="level-left"><button onClick={() => this.setState({confirm_delete: false})} type="button" className="button is-outlined">Cancel</button></div>
										<div className="level-right"><button onClick={this.handleDelete} type="button" className="button is-danger">Delete</button></div>
									</div>
								</div>
							</article>
						) : ""}	
					</form>
				</div>
			);
		}
	}
}
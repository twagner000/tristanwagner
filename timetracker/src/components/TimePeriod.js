import React from "react";
import { Link } from "react-router-dom";
import { ServiceContext } from "./TimeTrackerService";

export class TimePeriodSummary extends React.Component {
	static contextType = ServiceContext;
	
	state = {
		data: [],
		loaded: false,
		placeholder: "Loading...",
		per_start: "",
		per_end: ""
	};
	
	constructor(props) {
		super(props);
		
		const today = new Date();
		const monday = new Date(today);
		monday.setDate(today.getDate()-today.getDay()+(today.getDay()===0?-6:1));
		const sunday = new Date(monday);
		sunday.setDate(monday.getDate()+6);
		
		this.state.per_start = monday.toISOString().slice(0, 10);
		this.state.per_end = sunday.toISOString().slice(0, 10);
	}
	
	componentDidMount() {
		this.context.getTimePeriodSummary(this.state.per_start, this.state.per_end)
			.then(data => this.setState({ data: data, loaded: true }));
	}
	
	handleChange = (e) => this.setState({ [e.target.name]: e.target.value });
	
	handleSubmit = (e) => {
		this.setState({loaded: false});
		this.context.getTimePeriodSummary(this.state.per_start, this.state.per_end)
			.then(data => this.setState({ data: data, loaded: true }));
	};
	
	render() {
		const results = (!this.state.loaded) ? (<p>{this.state.placeholder}</p>) : (
			<div className="content">
				<h5>Results</h5>
				<p>{this.state.data.start} to {this.state.data.end}</p>
				<ul>
				{this.state.data.results.map((p,i) => (
					<li key={p.id}>[{p.hours.toFixed(2)}] {p.name}
						<ul>
						{p.tasks.map((t,i) => (
							<li key={t.id}>[{t.hours.toFixed(2)}] {t.full_name}
								<ul>
								{t.entries.map((e,i) => (
									<li key={e.id}>[{e.hours.toFixed(2)}] {e.start} to {e.end}</li>
								))}
								</ul>
							</li>
						))}
						</ul>
					</li>
				))}
				</ul>
			</div>
		)
			
		return (
			<div className="content">
				<Link to="/" className="delete is-pulled-right"></Link>
				<h5>Time Period Summary</h5>
				<div className="field">
					<label className="label">From</label>
					<div className="control">
						<input
							className="input"
							type="date"
							name="per_start"
							aria-label="Period Start"
							value={this.state.per_start}
							onChange={this.handleChange}
						/>
					</div>
				</div>
				<div className="field">
					<label className="label">To</label>
					<div className="control">
						<input
							className="input"
							type="date"
							name="per_end"
							aria-label="Period End"
							value={this.state.per_end}
							onChange={this.handleChange}
						/>
					</div>
				</div>
				<div className="field">
					<div className="control">
						<button onClick={this.handleSubmit} type="button" className="button is-primary is-fullwidth">Go</button>
					</div>
				</div>
				{results}
			</div>
		);
	}
}
import React from "react";
import { format } from 'date-fns';
import { Link, withRouter } from "react-router-dom";
import { ServiceContext } from "./TimeTrackerService";

export class TimePeriodSummary extends React.Component {
	static contextType = ServiceContext;
	
	constructor(props) {
		super(props);
		
		const today = new Date();
		const monday = new Date(today);
		monday.setDate(today.getDate()-today.getDay()+(today.getDay()==0?-6:1));
		const sunday = new Date(monday);
		sunday.setDate(monday.getDate()+6);
		
		this.state = {
			per_start: monday.toISOString().slice(0, 10),
			per_end: sunday.toISOString().slice(0, 10)
		};
	}
	
	handleChange = (e) => this.setState({ [e.target.name]: e.target.value });
	
	render() {
		return (
			<React.Fragment>
				<h5>Time Period Summary</h5>
				<div className="form-group" style={{display: "flex"}}>
					<input
						className="form-control"
						type="date"
						name="per_start"
						aria-label="Period Start"
						value={this.state.per_start}
						onChange={this.handleChange}
					/>
					<span className="btn">to</span>
					<input
						className="form-control"
						type="date"
						name="per_end"
						aria-label="Period End"
						value={this.state.per_end}
						onChange={this.handleChange}
					/>
				</div>
				<h5>Results</h5>
			</React.Fragment>
		);
	}
}
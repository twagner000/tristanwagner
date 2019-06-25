import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";
import { format } from 'date-fns';

class Entry extends React.Component {
	render() {
		if (this.props.data.end) {
			return (
				<React.Fragment>
					<div><a href="#" className="btn btn-outline-primary"><i className="fas fa-play"></i></a></div>
					<div><b>{this.props.data.task.full_name}</b><br/>{this.props.data.hours.toFixed(2)} hours ending {format(this.props.data.end, 'M/D/YY h:mma')}<br/><em>{this.props.data.comments}</em></div>
				</React.Fragment>
			);
		} else {
			return (
				<React.Fragment>
					<div><a href="#" className="btn btn-outline-danger"><i className="fas fa-stop"></i></a></div>
					<div><b>{this.props.data.task.full_name}</b><br/>Started {format(this.props.data.start, 'M/D/YY h:mma')}<br/><em>{this.props.data.comments}</em></div>
				</React.Fragment>
			);
		}
	}
}


class RecentEntries extends React.Component {
	static propTypes = {
		endpoint: PropTypes.string.isRequired,
		token: PropTypes.string.isRequired
	};
	
	constructor(props) {
		super(props);
		this.state = {
			data: [],
			loaded: false,
			placeholder: "Loading..."
		};
	}
	
	componentDidMount() {
		const headers = {
            'Content-Type': 'application/json',
			'Authorization': 'Token ' + this.props.token
        };

		fetch(this.props.endpoint, {headers})
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

//RecentEntries.propTypes = {};

export default RecentEntries;

/*  !data.length ? (
    <p>Nothing to show</p>
  ) : (
    <div className="column">
      <h2 className="subtitle">
        Showing <strong>{data.length} items</strong>
      </h2>
      <table className="table is-striped">
        <thead>
          <tr>
            {Object.entries(data[0]).map(el => <th key={key(el)}>{el[0]}</th>)}
          </tr>
        </thead>
        <tbody>
          {data.map(el => (
            <tr key={el.id}>
              {Object.entries(el).map(el => <td key={key(el)}>{el[1]}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

Table.propTypes = {
  data: PropTypes.array.isRequired
};

export default Table;*/
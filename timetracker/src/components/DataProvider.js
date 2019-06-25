import React, { Component } from "react";
import PropTypes from "prop-types";

class DataProvider extends Component {
	static propTypes = {
		endpoint: PropTypes.string.isRequired,
		render: PropTypes.func.isRequired
	};

	state = {
		data: [],
		loaded: false,
		placeholder: "Loading..."
	};

	componentDidMount() {
		const headers = {
            'Content-Type': 'application/json'
        }

        if (this.props.token) {
            headers['Authorization'] = 'Token ' + this.props.token;
        }

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
		const { token, data, loaded, placeholder } = this.state;
		return loaded ? this.props.render(data) : <p>{placeholder}</p>;
	}
}

export default DataProvider;
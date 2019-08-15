import React from 'react';
import {Link} from 'react-router-dom';
import {Content} from 'react-bulma-components';


export default class Search extends React.Component {
	render() {
		return (
			<Content>
				<h3>Search</h3>
				<p><Link to="/game/5">Game5</Link></p>
				<p><Link to="/">About</Link></p>
			</Content>
		)
	}
}
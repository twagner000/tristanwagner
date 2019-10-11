import React from 'react';
import {Redirect} from 'react-router-dom';
import {Content} from 'rbx';


class Home extends React.Component {
	render() {
		return (
			<Content>
				<p>Hello. Select a world above.</p>
				<Redirect to="/world/28" />
			</Content>
		);
	}
}


export default Home;
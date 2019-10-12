import React from 'react';
import {Redirect} from 'react-router-dom';
import {Content} from 'rbx';
import {connect} from 'react-redux';


class Home extends React.Component {
	render() {
		if (this.props.worlds.length) {
			return <Redirect to={`/world/${this.props.worlds[0].id}`} />
		} else {
			return (
				<Content>
					<p>Hello. Select a world above.</p>
				</Content>
			);
		}
	}
}

const mapStateToProps = state => {
	return {
		worlds: state.map.worlds,
	}
}

export default connect(mapStateToProps)(Home);
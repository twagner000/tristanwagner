import React from 'react';
import {PageLoader, Title} from 'rbx';
import {connect} from 'react-redux';

import {map} from "../actions";


class LoadWorld extends React.Component {
	componentDidMount() {
		this.props.fetchWorld(this.props.match.params.world_id);
	}
	
	componentDidUpdate() {
		if (!this.props.isFetchingWorld && this.props.world) {
			this.props.history.push('/map/face');
		}
	}
		
	render() {
		return <PageLoader color="white" active><Title>Loading world...</Title></PageLoader>;
	}
}

const mapStateToProps = state => {
	return {
		isFetchingWorld: state.map.isFetchingFace,
		world: state.map.world,
	}
}

const mapDispatchToProps = dispatch => {
	return {
        fetchWorld: (id) => dispatch(map.fetchWorld(id)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(LoadWorld);
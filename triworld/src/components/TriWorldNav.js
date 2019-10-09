import React from 'react';
import {Link} from 'react-router-dom';
import {Level, Button, Dropdown, Icon} from 'rbx';
import {connect} from 'react-redux';

import {map} from "../actions";

class TriWorldNav extends React.Component {
	componentDidMount() {
        this.props.fetchWorldList();
    }
	
	render() {
		return (
			<Level>
				<Level.Item>
					<Button as={Link} to="/"><Icon><i className="fas fa-hiking"></i></Icon><span>TriWorld</span></Button>
				</Level.Item>
				<Level.Item>
					<Dropdown>
						<Dropdown.Trigger>
							<Button>
								<Icon><i className="fas fa-globe"></i></Icon>
								<Icon size="small"><i className="fas fa-angle-down"></i></Icon>
							</Button>
						</Dropdown.Trigger>
						<Dropdown.Menu>
							<Dropdown.Content>
								{this.props.worlds.map((w,ci) => (
									<Dropdown.Item as={Link} to={`/map/f/${w.home_face_id}`} key={w.id}>{w.id} ({w.major_dim}x{w.minor_dim})</Dropdown.Item>
								))}
							</Dropdown.Content>
						</Dropdown.Menu>
					</Dropdown>
				</Level.Item>
				<Level.Item>
					<Button.Group hasAddons>
						<Button as={Link} to="/" state="active"><Icon><i className="fas fa-search-minus"></i></Icon></Button>
						<Button as={Link} to="/" disabled><Icon><i className="fas fa-search-plus"></i></Icon></Button>
						<Button as={Link} to="/" disabled><Icon><i className="fas fa-gem"></i></Icon></Button>
					</Button.Group>
				</Level.Item>
			</Level>
		);
	}
}

const mapStateToProps = state => {
	return {
		isFetchingWorldList: state.map.isFetchingWorldList,
		worlds: state.map.worlds,
	}
}

const mapDispatchToProps = dispatch => {
	return {
        fetchWorldList: () => dispatch(map.fetchWorldList()),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(TriWorldNav);
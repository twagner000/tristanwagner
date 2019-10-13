import React from 'react';
import {Link} from 'react-router-dom';
import {Level, Button, Dropdown, Icon} from 'rbx';
import {connect} from 'react-redux';

import {map} from "../actions";

class TriWorldNav extends React.Component {
	componentDidMount() {
        this.props.fetchWorldList();
    }
	
//<Level.Item><Icon><i className="fas fa-caret-square-down"></i></Icon></Level.Item>
	render() {
		return (
			<Level breakpoint="mobile">
				<Level.Item align="left">
					<Button.Group>
						<Button as={Link} to="/"><Icon><i className="fas fa-hiking"></i></Icon><span>TriWorld</span></Button>
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
										<Dropdown.Item key={w.id} as={Link} to={`/world/${w.id}`}>{w.id} ({w.major_dim}x{w.minor_dim})</Dropdown.Item>
									))}
								</Dropdown.Content>
							</Dropdown.Menu>
						</Dropdown>
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
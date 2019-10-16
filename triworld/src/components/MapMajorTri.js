import React from 'react';
import {Link} from 'react-router-dom';
import {Content, Icon, Media, Level, Button, Column, PageLoader, Title} from 'rbx';
import {connect} from 'react-redux';

import { MAP_FACE } from "../constants/routes";
import {map} from "../actions";

const MapSection = (props) => {
	return (
		null
	);
}

class MapMajorTri extends React.Component {
	/*constructor(props) {
		super(props);
		this.handleClick = this.handleClick.bind(this);
	}
	
	componentDidMount() {
		if (!this.props.world) {
			this.props.history.push('/');
		}
		if (!this.props.selectedMajorTri) {
			this.props.history.push(MAP_FACE);
		}
	}
	
	handleClick(id) {
		return (e) => {
			this.props.selectMinorTri(id);
		}
	}*/
	
	render() {
		if (!this.props.world) {
			return ""
		} else {
			const n = this.props.world.major_dim;
			const face = this.props.currentFace;
			const mw = 400; //map width for svg scaling
			const v_margin = 20;
			const h_margin = 5;
			const fpd = face.fpd;
			const b = (mw-2*h_margin)/(8/3*n)*2; //scale triangle size
			const h = b*Math.sqrt(3)/2;
			
			const p = {n,fpd,mw,b,h};
			
			return (
				<Column.Group>
					<Column>
						<Level>
							<Level.Item>
								<Button.Group hasAddons>
									<Button as={Link} to={MAP_FACE}><Icon><i className="fas fa-search-minus"></i></Icon></Button>
									<Button disabled><Icon><i className="fas fa-gem"></i></Icon></Button>
								</Button.Group>
							</Level.Item>
						</Level>
						<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="100%" viewBox={`0 0 ${mw} ${mw}`}>
							<g transform={`translate(${h_margin} ${v_margin})`}>
								<MapSection p={p} handleClick={this.handleClick} />
								<MapSection p={p} handleClick={this.handleClick} />
								<MapSection p={p} handleClick={this.handleClick} />
								<MapSection p={p} handleClick={this.handleClick} />
							</g>
						</svg>
					</Column>
					<Column>
						<Content>
							<h5>Face {face.id} ({face.ring}, {face.ring_i})</h5>
							<h5>Selected MajorTri {this.props.currentMajorTri && this.props.currentMajorTri.id}</h5>
							{!this.props.currentMajorTri || !this.props.currentMajorTri.neighbor_ids ? "" : (							
								<table className="table">
									<tbody>
									{Object.entries(this.props.currentMajorTri.neighbor_ids).map((v) => (
										<tr key={v[0]}><th>{v[0]}</th><td>{v[1]}</td></tr>
									))}
									</tbody>
								</table>
							)}
							<p>{JSON.stringify(this.props.currentMajorTri).replace(/,"/g,', "')}</p>
							
						</Content>
					</Column>
				</Column.Group>
			);
		}
	}
}

const mapStateToProps = state => {
	return {
		world: state.map.world,
		currentFace: state.map.currentFace,
		currentMajorTri: state.map.currentMajorTri,
	}
}

const mapDispatchToProps = dispatch => {
	return {
        selectFace: (id) => dispatch(map.selectFace(id)),
        selectMajorTri: (id) => dispatch(map.selectMajorTri(id)),
        selectMinorTri: (id) => dispatch(map.selectMinorTri(id)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(MapMajorTri);
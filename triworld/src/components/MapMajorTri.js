import React from 'react';
import {Link} from 'react-router-dom';
import {Content, Icon, Media, Level, Button, Column, PageLoader, Title} from 'rbx';
import {connect} from 'react-redux';

import { MAP_FACE } from "../constants/routes";
import {map} from "../actions";

const MapSection = (props) => {
	const tpd = !(props.angle%120);
	const {b,h} = props.p;
	
	return (
		<g transform={`translate(${!(props.angle%180)?-b/2:(props.angle<180?0:-b)} ${(props.angle===0||props.angle===60||props.angle===300)?-h:0})`}>
			<path d={`M 0 ${tpd?0:h} h ${b} l ${-b/2} ${tpd?h:-h} z`} className="face-outline" />
			<text x={b/2} y={h/2} className="tri-text" dominantBaseline="middle" textAnchor="middle">{props.tri && props.tri.id}</text>
		</g>
	);
}

class MapMajorTri extends React.Component {
	constructor(props) {
		super(props);
		this.handleClick = this.handleClick.bind(this);
	}
	
	componentDidMount() {
		if (!this.props.world) {
			this.props.history.push('/');
		}
		if (!this.props.currentMajorTri) {
			this.props.history.push(MAP_FACE);
		}
	}
	
	handleClick(id) {
		return (e) => {
			this.props.selectMinorTri(id);
		}
	}
	
	render() {
		if (!this.props.world) {
			return ""
		} else {
			const sn = this.props.world.minor_dim;
			const mw = 400; //map width for svg scaling
			const v_margin = 20;
			const h_margin = 5;
			const b = (mw-2*h_margin)/2; //scale triangle size
			const h = b*Math.sqrt(3)/2;
			
			const p = {sn,mw,b,h};
			
			const tri = this.props.currentMajorTri;
			
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
						<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="100%" viewBox={`${-mw/2} ${-mw/2} ${mw} ${mw}`}>
							<MapSection angle={0} tri={tri.tpd?tri:null} p={p} handleClick={this.handleClick} />
							<MapSection angle={60} p={p} handleClick={this.handleClick} />
							<MapSection angle={120} p={p} handleClick={this.handleClick} />
							<MapSection angle={180} tri={!tri.tpd?tri:null} p={p} handleClick={this.handleClick} />
							<MapSection angle={240} p={p} handleClick={this.handleClick} />
							<MapSection angle={300} p={p} handleClick={this.handleClick} />
						</svg>
					</Column>
					<Column>
						<Content>
							<h5>Selected MajorTri {this.props.currentMajorTri.id}</h5>
							{!this.props.currentMajorTri || !this.props.currentMajorTri.cached_neighbor_ids ? "" : (							
								<table className="table">
									<tbody>
									{Object.entries(this.props.currentMajorTri.cached_neighbor_ids).map((v) => (
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
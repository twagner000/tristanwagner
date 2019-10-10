import React from 'react';
import {Link} from 'react-router-dom';
import {Content, Icon, Media, Level, Button, Column} from 'rbx';
import {connect} from 'react-redux';

import {map} from "../actions";

class AdjFaceLink extends React.Component {
	render() {
		//const color_list = {"top":"#f00", "left":"#0f0", "right":"#00f", "default":"#000"};
		//const color = (this.props.direction && this.props.direction in color_list) ? color_list[this.props.direction] : "default";
		
		const r = 10;
		return (
			<Link to={`/map/f/${this.props.face_id}`}>
				<circle r={r} className="adj-face-circle" />
			</Link>
		);
	}
}

class MajorTri extends React.Component {
	
	render() {
		const tri = this.props.tri;
		const b = this.props.base;
		const h = this.props.height;
		return (
			<g onClick={this.props.handleClick(this)} className="tri-g">
				<path key={tri.id} d={"M 0 "+(tri.tpd ? 0 : h)+" h "+b+" l "+(-b/2)+" "+(tri.tpd ? h : -h)+" z"} className={"tri"+(tri.sea ? " tri-sea" : " tri-land")} />
				<text x={b/2} y={h/3} className="tri-text" dominantBaseline="middle" textAnchor="middle">{tri.face}</text>
				<text x={b/2} y={h*2/3} className="tri-text" dominantBaseline="middle" textAnchor="middle">{tri.major_row},{tri.major_col}</text>
			</g>
		);
	}
}

class MapFace extends React.Component {
	state = {tri_selected: null};
	
	constructor(props) {
		super(props);
		this.handleClick = this.handleClick.bind(this);
	}
	
	checkForUpdate = () => {
		const face_id = parseInt(this.props.match.params.face_id);
		if (face_id !== (this.props.activeFace && this.props.activeFace.id) && !this.props.isFetchingFace) {
			this.props.fetchFace(face_id);
		}
	}
		
	componentDidMount() {
        this.checkForUpdate();
    }
	
	componentDidUpdate() {
		this.checkForUpdate();
    }
	
	handleClick(tri) {
		return (e) => {
			this.setState({tri_selected: tri.props.tri});
		}
	}
	
	render() {
		const face = this.props.activeFace;
		if (!face) {
			return "";
		} else {
			const box_width = 400;
			const v_margin = 30;
			const h_margin = 10;
			const n = face.major_dim;
			const fpd = face.points_down; //face points down
			const b = (box_width-2*h_margin)/(8/3*n)*2; //scale triangle size
			const h = b*Math.sqrt(3)/2;
			const rows = face.map;
			for (let ri=0; ri<rows.length; ri++) {
				for (let ci=0; ci<rows[ri].length; ci++) {
					rows[ri][ci].tpd = (ci+parseInt(2*ri/rows.length))%2>0;
				}
			}
			
			//alt underground ideas: gem (not in fontawesome: stairs, pick/shovel)
			//<rect width="100%" height="100%" style={{fill: 'none', strokeWidth: 1, stroke: '#000'}} />
			return (
				<Column.Group>
					<Column>
						<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width={box_width} height={box_width}>
							<g transform={`translate(${h_margin} ${v_margin})`}>
								{rows.map((r,ri) => (
									<g key={ri} transform={"translate("+((Math.abs(2/3*n-.5-ri)-.5)*b/2)+" "+(ri*h)+")"}>
										{r.map((c,ci) => (
											<g key={ci} transform={"translate("+b*ci/2+" 0)"}>
										<MajorTri tri={c} base={b} height={h} handleClick={this.handleClick} />
											</g>
										))}
									</g>
								))}
								<g transform={`translate(${b*n*2/3} ${fpd?0:h*n*4/3})`}><AdjFaceLink direction="top" face_id={face.neighbor_ids.top_bot} /></g>
								<g transform={`translate(${b*n/6} ${fpd?h*n:h*n/3})`}><AdjFaceLink direction="left" face_id={face.neighbor_ids.left} /></g>
								<g transform={`translate(${b*n*7/6} ${fpd?h*n:h*n/3})`}><AdjFaceLink direction="right" face_id={face.neighbor_ids.right} /></g>
							</g>
						</svg>
					</Column>
					<Column>
						<Content>
							<h5>Face</h5>
							<table className="table">
								<tbody>
									<tr><th>ID</th><td>{face.id}</td></tr>
									<tr><th>Ring</th><td>{face.face_ring}</td></tr>
									<tr><th>Index</th><td>{face.face_index}</td></tr>
								</tbody>
							</table>
							<h5>Selected MajorTri</h5>
							<p>{JSON.stringify(this.state.tri_selected).replace(/,"/g,', "')}</p>
						</Content>
					</Column>
				</Column.Group>
			);
		}
	}
}

const mapStateToProps = state => {
	return {
		activeFace: state.map.activeFace,
		faces: state.map.faces,
		isFetchingFace: state.map.isFetchingFace,
	}
}

const mapDispatchToProps = dispatch => {
	return {
        fetchFace: (id) => dispatch(map.fetchFace(id)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(MapFace);
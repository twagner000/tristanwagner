import React from 'react';
import {Link} from 'react-router-dom';
import {Content, Icon, Media, Level, Button, Column} from 'rbx';
import {connect} from 'react-redux';

import {mapface} from "../actions";

class AdjFaceLink extends React.Component {
	render() {
		//const color_list = {"top":"#f00", "left":"#0f0", "right":"#00f", "default":"#000"};
		//const color = (this.props.direction && this.props.direction in color_list) ? color_list[this.props.direction] : "default";
		
		//<g transform="rotate(0)"><path d={`M ${-r} 0 l ${r} ${-r} l ${r} ${r} z`} style={{stroke: "#000", strokeWidth: 2, fill: "#eee"}} /></g>
		//<text className="tri-text" dominantBaseline="middle" textAnchor="middle">{this.props.direction[0].toUpperCase()}</text>
		
		const r = 10;
		return (
			<Link to={"/w/"+this.props.world_id+"/map/f/"+this.props.face_id}>
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
			<g onClick={this.props.handleClick(this)}>
				<path key={tri.id} d={"M 0 "+(tri.tpd ? 0 : h)+" h "+b+" l "+(-b/2)+" "+(tri.tpd ? h : -h)+" z"} className={"tri"+(tri.sea ? " tri-sea" : " tri-land")} />
				<text x={b/2} y={h/2} className="tri-text" dominantBaseline="middle" textAnchor="middle">{tri.major_row},{tri.major_col}</text>
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
		if (!this.props.isFetchingMap && (this.props.map == null || parseInt(this.props.match.params.world_id) !== this.props.map.world_id || parseInt(this.props.match.params.face_id) !== this.props.map.id)) {
			this.props.loadMapFace(this.props.match.params.world_id,this.props.match.params.face_id);
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
		const map = this.props.map;
		if (!map) {
			return "";
		} else {
			const box_width = 400;
			const v_margin = 30;
			const h_margin = 10;
			const n = this.props.map.major_dim;
			const fpd = this.props.map.points_down; //face points down
			const b = (box_width-2*h_margin)/(8/3*n)*2; //scale triangle size
			const h = b*Math.sqrt(3)/2;
			const rows = this.props.map.map;
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
							{rows.map((r,ri) => (
								<g key={ri} transform={"translate("+(h_margin+(Math.abs(2/3*n-.5-ri)-.5)*b/2)+" "+(v_margin+ri*h)+")"}>
									{r.map((c,ci) => (
										<g key={ci} transform={"translate("+b*ci/2+" 0)"}>
									<MajorTri tri={c} base={b} height={h} handleClick={this.handleClick} />
										</g>
									))}
									{((ri===0 && fpd) || (ri===rows.length-1 && !fpd)) ? <g transform={"translate("+(b/2*(r.length/2+.5))+" "+(fpd?0:h)+")"}><AdjFaceLink direction="top" world_id={this.props.match.params.world_id} face_id={this.props.map.neighbor_ids.top} /></g> : "" }
									{((ri===rows.length*3/4 && fpd) || (ri===rows.length/4 && !fpd)) ? <g transform={"translate("+(fpd ? 0 : b*r.length/2)+" 0)"}><AdjFaceLink direction="left" world_id={this.props.match.params.world_id} face_id={this.props.map.neighbor_ids.left} /></g> : "" }
									{((ri===rows.length*3/4 && fpd) || (ri===rows.length/4 && !fpd)) ? <g transform={"translate("+(!fpd ? b/2 : b*(r.length+1)/2)+" 0)"}><AdjFaceLink direction="right" world_id={this.props.match.params.world_id} face_id={this.props.map.neighbor_ids.right} /></g> : "" }
								</g>
							))}
						</svg>
					</Column>
					<Column>
						<Content>
							<h5>Selected MajorTri</h5>
							{this.state.tri_selected ? (
								<table className="table">
									<tbody>
										<tr><th>ID</th><td>{this.state.tri_selected.id}</td></tr>
										<tr><th>Row</th><td>{this.state.tri_selected.major_row}</td></tr>
										<tr><th>Col</th><td>{this.state.tri_selected.major_col}</td></tr>
										<tr><th>Sea</th><td>{this.state.tri_selected.sea.toString()}</td></tr>
										<tr><th>Fields</th><td>{Object.keys(this.state.tri_selected).join(', ')}</td></tr>
									</tbody>
								</table>
							) : ""}
						</Content>
					</Column>
				</Column.Group>
			);
		}
	}
}

const mapStateToProps = state => {
	return {
		map: state.mapface.map,
		isFetchingMap: state.mapface.isFetchingMap,
	}
}

const mapDispatchToProps = dispatch => {
	return {
        loadMapFace: (world_id,face_id) => {
			dispatch(mapface.startMapFaceRefresh());
            dispatch(mapface.fetchMapFace(world_id,face_id));
        },
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(MapFace);
import React from 'react';
import {Link} from 'react-router-dom';
import {Content, Icon, Media, Level, Button} from 'rbx';
import {connect} from 'react-redux';

import {mapface} from "../actions";

class MapFace extends React.Component {
	checkForUpdate = () => {
		if (!this.props.isFetchingMap && (this.props.map == null || parseInt(this.props.match.params.world) !== this.props.map.world_id || parseInt(this.props.match.params.ring) !== this.props.map.face_ring || parseInt(this.props.match.params.index) !== this.props.map.face_index)) {
			this.props.loadMapFace(this.props.match.params.world,this.props.match.params.ring,this.props.match.params.index);
		}
	}
		
	componentDidMount() {
        this.checkForUpdate();
    }
	
	componentDidUpdate() {
		this.checkForUpdate();
    }
	
	render() {
		let map = this.props.map;
		if (!map) {
			return "";
		} else {
			const box_width = 400;
			const margin = 10;
			const n = this.props.map.major_dim;
			const b = (box_width-2*margin)/(8/3*n)*2; //scale triangle size
			const h = b*Math.sqrt(3)/2;
			const rows = this.props.map.map;
			
			//alt underground ideas: gem (not in fontawesome: stairs, pick/shovel)
			//<rect width="100%" height="100%" style={{fill: 'none', strokeWidth: 1, stroke: '#000'}} />
			return (
				<Content align="center">
					<p><Link to="/"><Icon size="large"><i className="fas fa-chevron-up fa-2x" style={{transform: "rotate(60deg)"}}></i></Icon></Link></p>
					<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width={box_width} height={box_width}>
						{rows.map((r,ri) => (
						<g key={ri} transform={"translate("+(margin+(Math.abs(2/3*n-.5-ri)-.5)*b/2)+" "+(margin+ri*h)+")"}>
								{r.map((c,ci) => (
									<g key={ci} transform={"translate("+b*ci/2+" 0)"}>
										<path key={ci} d={"M 0 "+((c && c.points_down) ? 0 : h)+" h "+b+" l "+(-b/2)+" "+((c && c.points_down) ? h : -h)+" z"} className={"tri"+(c ? (c.sea ? " tri-sea" : " tri-land") : "")} />
										<text x={b/2} y={h/2} className="tri-text" dominantBaseline="middle" textAnchor="middle">{c && c.major_row},{c && c.major_col}</text>
									</g>
								))}
							</g>
						))}
					</svg>
				</Content>
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
        loadMapFace: (world,ring,index) => {
			dispatch(mapface.startMapFaceRefresh());
            dispatch(mapface.fetchMapFace(world,ring,index));
        },
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(MapFace);
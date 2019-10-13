import React from 'react';
import {Link, Redirect} from 'react-router-dom';
import {Content, Icon, Media, Level, Button, Column, PageLoader, Title} from 'rbx';
import {connect} from 'react-redux';

import {map} from "../actions";

const AdjFaceLink = (props) => {
	const r = 15;
	const b = r*Math.sqrt(3)/2;
	return (
		<g className="button" transform={`rotate(${props.rotation})`} onClick={() => props.handleClick(props.face_id)}>
			<circle r={r} className="adj-face-circle"/>
			<path d={`M ${-b} ${r/2} l ${b} ${-r} l ${b} ${r}`} className="adj-face-circle"/>
		</g>
	);
}

const MajorTri = (props) => {
	const tri = props.tri;
	const b = props.base;
	const h = props.height;
	//<text x={b/2} y={h/3} className="tri-text" dominantBaseline="middle" textAnchor="middle">{tri.id}</text>
	return (
		<g onClick={props.handleClick(tri.id)} className="tri-g">
			<path d={`M 0 ${tri.tpd?0:h} h ${b} l ${-b/2} ${tri.tpd?h:-h} z`} className={"tri"+(tri.sea ? " tri-sea" : " tri-land")} />
			<text x={b/2} y={h*2/3} className="tri-text" dominantBaseline="middle" textAnchor="middle">{tri.i}</text>
		</g>
	);
}

const FaceSection = (props) => {
	const { n, fpd, b, h } = props.p;
	
	//cfpd means 'current face points down' VISUALLY (fpd and ring refer to the center face)
	const cfpd = (props.section==="center") ? fpd : !fpd;
	
	const calc = {
		"top_bot":{
			origin:`translate(${b*n/6} ${fpd?-h*n*2/3:h*n})`,
			outline:`M 0 ${fpd?h*n:0} h ${b*n} l ${-b} ${fpd?-h*n/3:h*n/3} h ${-b*n*2/3} z`,},
		"left":{
			origin:`translate(${-b*n/3} ${fpd?h*n/3:0})`,
			outline:`M ${b*n/2} ${fpd?0:h*n} l ${-b*n/6} ${fpd?h*n/3:-h*n/3} l ${b*n/3} ${fpd?h*n*2/3:-h*n*2/3} h ${b*n/3} z`,},
		"right":{
			origin:`translate(${b*n*2/3} ${fpd?h*n/3:0})`,
			outline:`M ${b*n/2} ${fpd?0:h*n} l ${b*n/6} ${fpd?h*n/3:-h*n/3} l ${-b*n/3} ${fpd?h*n*2/3:-h*n*2/3} h ${-b*n/3} z`,},
		"center":{
			origin:`translate(${b*n/6} ${fpd?h*n/3:0})`,
			outline:`M 0 ${fpd?0:h*n} h ${b*n} l ${-b*n/2} ${fpd?h*n:-h*n} z`,},};
	
	for (const tri of props.tris) {
		//basic row and column indices, if face points up (pu) or down (pd) visually
		const ripu = parseInt(Math.sqrt(tri.i));
		const ripd = n-1-parseInt(Math.sqrt(n*n-1-tri.i));
		const cipu = tri.i-ripu*ripu;
		const cipd = tri.i-(n*n-(n-ripd)*(n-ripd));
		
		tri.ri = (cfpd) ? ripd : ripu;
		tri.ci = (cfpd) ? cipd : cipu;
		
		//special rotations for polar side faces
		if (props.ring===0 && props.section==="left") {
			tri.ri = parseInt((tri.i-ripu*ripu)/2);
			tri.ci = 2*n-2 - 2*ripu + cipu%2;
		} else if (props.ring===0 && props.section==="right") {
			tri.ri = parseInt(((ripu+1)*(ripu+1)-tri.i-1)/2)
			tri.ci = cipu;
		} else if (props.ring===3 && props.section==="left") {
			tri.ri = n-1-parseInt((tri.i - (n*n - (n-ripd)*(n-ripd)))/2);
			tri.ci = 2*ripd + (tri.i-(n*n-(n-ripd)*(n-ripd)))%2;
		} else if (props.ring===3 && props.section==="right") {
			tri.ri = n-1-parseInt((n*n - (n-1-ripd)*(n-1-ripd) -tri.i-1)/2)
			tri.ci = cipd;
		}
		
		tri.rn = cfpd ? 2*n-1-2*tri.ri : tri.ri*2+1;
		
		//tpd means 'triangle points down'
		tri.tpd = cfpd !== (tri.ci%2>0);
	}
	
	//filter just the relevant triangles for this view
	const tris = props.tris.filter((tri) => { switch (props.section) {
		case "top_bot": return fpd ? tri.i>=n*n*4/9 : tri.i<n*n*5/9;
		case "left": return tri.ci >= tri.rn - n*2/3;
		case "right": return tri.ci < n*2/3;
		default: return true;
	}});
	
	return (
		<g transform={calc[props.section].origin} className={`face face-${props.section.replace("_","-")}`}>
			{tris.map((tri) => (
				<g key={tri.id} transform={`translate(${cfpd?b*tri.ri/2+b*tri.ci/2:b*(n-1-tri.ri)/2+b*tri.ci/2} ${h*tri.ri})`}>
					<MajorTri tri={tri} base={b} height={h} handleClick={props.handleClick} />
				</g>
			))}
			<path d={calc[props.section].outline} className="face-outline" />
		</g>
	);
}

class MapFace extends React.Component {
	constructor(props) {
		super(props);
		this.handleClick = this.handleClick.bind(this);
	}
	
	componentDidMount() {
		if (!this.props.world) {
			this.props.history.push('/');
		}
	}
	
	handleClick(id) {
		return (e) => {
			this.props.selectMajorTri(id);
		}
	}
	
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
									<Button as={Link} to="/" state="active"><Icon><i className="fas fa-search-minus"></i></Icon></Button>
									<Button as={Link} to="/" disabled><Icon><i className="fas fa-search-plus"></i></Icon></Button>
									<Button as={Link} to="/" disabled><Icon><i className="fas fa-gem"></i></Icon></Button>
								</Button.Group>
							</Level.Item>
						</Level>
						<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="100%" viewBox={`0 0 ${mw} ${mw}`}>
							<g transform={`translate(${h_margin} ${v_margin})`}>
								<FaceSection section="top_bot" ring={face.ring} tris={this.props.world.faces[face.neighbor_ids.top_bot].majortris} p={p} handleClick={this.handleClick} />
								<FaceSection section="left" ring={face.ring} tris={this.props.world.faces[face.neighbor_ids.left].majortris} p={p} handleClick={this.handleClick} />
								<FaceSection section="right" ring={face.ring} tris={this.props.world.faces[face.neighbor_ids.right].majortris} p={p} handleClick={this.handleClick} />
								<FaceSection section="center" ring={face.ring} tris={face.majortris} p={p} handleClick={this.handleClick} />
								
								<g transform={`translate(${b*n*2/3} ${fpd?0:h*n*4/3})`}><AdjFaceLink rotation={fpd?0:180} face_id={face.neighbor_ids.top_bot} handleClick={this.props.selectFace} /></g>
								<g transform={`translate(${b*n/6} ${fpd?h*n:h*n/3})`}><AdjFaceLink rotation={fpd?-120:-60} face_id={face.neighbor_ids.left} handleClick={this.props.selectFace} /></g>
								<g transform={`translate(${b*n*7/6} ${fpd?h*n:h*n/3})`}><AdjFaceLink rotation={fpd?120:60} face_id={face.neighbor_ids.right} handleClick={this.props.selectFace} /></g>
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
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(MapFace);
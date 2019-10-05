import React from 'react';
import {Link} from 'react-router-dom';
import {Content, Icon, Media, Level, Table} from 'rbx';
import {connect} from 'react-redux';

import {games} from "../actions";

class MapFace extends React.Component {
	render() {
		let n = 6;
		let row_n = [9,11,13,15,15,13,11,9];
		let b = 30;
		let h = b*Math.sqrt(3)/2;
		let rows = new Array(row_n.length).fill(undefined).map((_,i) => new Array(row_n[i]).fill(undefined).map((_,j) => {return {sea: Math.random()<1/3, down:(i<2/3*n)===(j%2!==0)};}));
		return (
			<Content>
				<Link to="/" className="is-pulled-right delete"></Link>
				<h4>Map</h4>
				<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="400" height="400">
					<rect width="100%" height="100%" style={{fill: 'none', strokeWidth: 1, stroke: '#000'}} />
					{rows.map((r,ri) => (
					<g key={ri} transform={"translate("+(Math.abs(2/3*n-.5-ri)-.5)*b/2+" "+ri*h+")"}>
							{r.map((c,ci) => (
								<g key={ci} transform={"translate("+b*ci/2+" 0)"}>
									<path key={ci} d={"M 0 "+(c.down ? 0 : h)+" h "+b+" l "+(-b/2)+" "+(c.down ? h : -h)+" z"} className={"tri"+(c.sea ? " tri-sea" : " tri-land")} />
								</g>
							))}
						</g>
					))}
				</svg>
			</Content>
		);
	}
}

const mapStateToProps = state => {
	return {
		game: state.games.game,
		isFetchingGame: state.games.isFetchingGame,
	}
}

const mapDispatchToProps = dispatch => {
	return {
        loadGame: (id) => {
			dispatch(games.startGameRefresh());
            dispatch(games.fetchGame(id));
        },
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(MapFace);
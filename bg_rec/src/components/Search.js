import React from 'react';
import {withRouter} from 'react-router-dom';
import {Field} from 'rbx';
import {components as SelectComponents} from 'react-select';
import AsyncSelect from 'react-select/async';
import {connect} from 'react-redux';

import {games} from "../actions";

//https://github.com/JedWatson/react-select/issues/3128#issuecomment-451936743
const Option = ({ children, ...props }) => {
	const { onMouseMove, onMouseOver, ...rest } = props.innerProps;
	const newProps = Object.assign(props, { innerProps: rest });
	return (
		<SelectComponents.Option {...newProps} className="select-item-hover" >
			{children}
		</SelectComponents.Option>
	);
};

class Search extends React.Component {
	componentDidMount() {
        this.props.fetchGames();
    }
	
	handleChange = (option, meta) => {
		if (option) {
			this.props.history.push(`/game/${option.objectid}/`);
		}
	}
	
	filterGames = (inputValue: string) => {
		return this.props.gameList.filter(i =>
			i.name.toLowerCase().includes(inputValue.toLowerCase())
		);
	};

	loadOptions = (inputValue, callback) => {
		setTimeout(() => {
			callback(this.filterGames(inputValue));
		}, 500);
	};
	
	render() {
		//AsyncSelect for speed
		return (
			<Field>
				<AsyncSelect
					cacheOptions
					defaultOptions
					loadOptions={this.loadOptions}
					className="control"
					name="game"
					aria-label="Game"
					placeholder="Select a game..."
					required
					getOptionLabel={option => option.name}
					getOptionValue={option => option.objectid}
					onChange={this.handleChange}
					autoFocus
					components={{Option}}
				/>
			</Field>
		)
	}
}

const mapStateToProps = state => {
	return {
		gameList: state.games.gameList,
		gameListLoaded: state.games.gameListLoaded,
	}
}

const mapDispatchToProps = dispatch => {
	return {
        fetchGames: () => {
            dispatch(games.fetchGames());
        },
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(withRouter(Search));
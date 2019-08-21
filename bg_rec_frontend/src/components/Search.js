import React from 'react';
import {withRouter} from 'react-router-dom';
import {Form} from 'react-bulma-components';
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
			<React.Fragment>
				<Form.Field>
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
				</Form.Field>
			</React.Fragment>
		)
		/*					<Select
						className="control is-expanded"
						name="game"
						aria-label="Game"
						placeholder="Select a game..."
						required
						options={this.props.gameList}
						getOptionLabel={option => option.name}
						getOptionValue={option => option.objectid}
						onChange={this.handleChange}
						autoFocus
						components={{Option}}
						filterOption={createFilter({ignoreAccents: false})}
					/>*/
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
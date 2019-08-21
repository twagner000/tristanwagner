import React from 'react';
import {withRouter} from 'react-router-dom';
import {Form} from 'react-bulma-components';
import Select, {createFilter, components as SelectComponents} from 'react-select';
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
	
	render() {
		//filterOption because of https://github.com/JedWatson/react-select/issues/3128#issuecomment-431397942
		return (
			<React.Fragment>
				<Form.Field kind="addons">
					<Select
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
					/>
				</Form.Field>
			</React.Fragment>
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
import React from 'react';
import {Link} from 'react-router-dom';
import {Content, Button} from 'rbx';

const Home = () => {
	return (
		<Content>
			<p>Hello.</p>
			<p><Button as={Link} to="/w/13/map/f/226">6x6 Map</Button></p>
			<p><Button as={Link} to="/w/14/map/f/266">9x9 Map</Button></p>
			<p><Button as={Link} to="/w/15/map/f/286">6x9 Map</Button></p>
		</Content>
	)
}

export default Home
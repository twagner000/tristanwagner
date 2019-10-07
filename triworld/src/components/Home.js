import React from 'react';
import {Link} from 'react-router-dom';
import {Content, Button} from 'rbx';

const Home = () => {
	return (
		<Content>
			<p>Hello.</p>
			<p><Button as={Link} to="/w/12/map/f/206">Map</Button></p>
		</Content>
	)
}

export default Home
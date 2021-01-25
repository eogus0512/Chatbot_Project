import React, { Component } from 'react';
import { Box, Typography } from '@material-ui/core';
import logo from '../images/logo.png';

class Header extends Component<{}> {
	constructor(props: {}) {
		super(props);
	}

	render() {
		const flexRow: React.CSSProperties = { display: 'flex', flexDirection: 'row' };
        const flexColumn: React.CSSProperties = { display: 'flex', flexDirection: 'column' };
        
		const header:React.CSSProperties = {
            textAlign: 'center',
            lineHeight: '60px',
			fontSize: '20px',
			fontWeight: 'bold',
		};

		return (
			<Box
				style={{
					...flexRow,
					justifyContent: 'center',
					width: '100%',
					height: '60px',
					background: '#F6BB43',
				}}
			>
				<Box style={{ ...header}}>동국대학교 맛집 추천 챗봇</Box>
			</Box>
		);
	}
}
export default Header;

import React, { Component } from 'react';
import { Box, TextField, Typography, Button } from '@material-ui/core';
import axios from 'axios';

class HomeContainer extends Component<{}, any> {
	constructor(props: any) {
		super(props);
		this.state = {
			messages: [],
			message: '',
		};
	}


	postChatbot = (message: any) => {
		axios.post(
			`http://127.0.0.1:5000/query/TEST`,{
			data : { query : message }},
		);
	}

	handleMessages = (text : string) => {
		let messages = this.state.messages;
		this.postChatbot(text);
		this.setState({
			messages : [...messages, {"chat" : text, "isChat" : true}],
			message: ''
		})
	}

	handleChatInputKeyPress = (e: any) => {
		if (e.key == 'Enter' && e.target.value != '') {
			this.handleMessages(this.state.message);
		}
	};

	onClickButton = (e: any) => {
		this.handleMessages(this.state.message);
	};

	handleEditor = (e: any) => {
		this.setState({
			[e.target.id]: e.target.value,
		});
		console.log(`e.target.id`, e.target.value);
	};
	/*
	componentDidMount(){
		let message;
		const addPost = (message) =>
		axios.post(
			`http://127.0.0.1:5000/query/TEST`,
			{ message },
			{
				body: { quert: message },
			}
		);
	}
*/
	render() {
		const flexRow: React.CSSProperties = { display: 'flex', flexDirection: 'row' };
		const flexColumn: React.CSSProperties = { display: 'flex', flexDirection: 'column' };
		const messageOutsideBox: React.CSSProperties = { display: "inline-block", textAlign:"center",fontSize:"17px",
		border: "0px #0003 solid", padding: "5px 11px", margin:"4px 10px", boxSizing: "border-box", borderRadius: "7px", background: "#FFDBC1"};
		const messages = this.state.messages;

		return (
			<Box>
				<Box style={{ ...flexColumn, justifyContent: 'flex-start', minHeight: '85vh', width: '100%' }}>
					{messages.map((value : any) =>{
						return(
							<Box style={{...flexRow, justifyContent: "flex-end"}}>
							<Box style={{position: "relative", display: "inline-block"}}>
							<div style={value.isChat ? {...messageOutsideBox} : {...messageOutsideBox}}>
								{value.chat}
							</div>
							</Box>
							</Box>
						)
					})}
				</Box>
				<Box style={{ ...flexRow, justifyContent: 'space-around', width: '100%' }}>
					<TextField
						id="message"
						label="챗봇에게 질문하세요"
						onChange={this.handleEditor}
						variant="outlined"
						value={this.state.message}
						onKeyPress={this.handleChatInputKeyPress}
						autoFocus={true}
						style={{ width: '90%' }}
					></TextField>
					<button
						id="message"
						onClick={this.onClickButton}
						style={{ width: '9%', height: '6vh', background: '#F6BB43', borderRadius: '8px', border: 'none', fontSize: '15px', fontWeight: 'bold' }}
					>
						전송
					</button>
				</Box>
			</Box>
		);
	}
}
export default HomeContainer;

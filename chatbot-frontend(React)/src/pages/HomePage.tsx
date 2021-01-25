import React,{ Component} from 'react';
import Header from '../components/Header';
import HomeContainer from '../containers/HomeContainer';
import{ Box, Typography} from '@material-ui/core';

class HomePage extends Component<{}> {
    constructor(props: {}){
        super(props);
    }
    render(){
        return(
            <Box>
                    <Header></Header>
                    <HomeContainer></HomeContainer>
            </Box>
        )
    }
}
export default HomePage;
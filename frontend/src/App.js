import React from 'react';
import { v4 as uuidv4 } from 'uuid';
import _ from 'lodash';


import {Container} from 'reactstrap';

import StartPage from './StartPage';
import UserInfoForm from './UserInfoForm';
import StepList from './StepGenerator';
import getPolicyData from './transformCsvFiles';
import policy_data_path from './COVID_and_LAHSA_datasets/COVID/UK_1360beds-25policies.csv';
import { csv } from 'd3-fetch';
import TopNavBar from './TopNavBar';
import './Card.scss';
import axios from 'axios';
import EndPage from './EndPage';

// const SERVER_URL = "http://localhost:3004";
const SERVER_URL = "http://localhost:8000";

class App extends React.Component {
  constructor(props){
    super(props)
    this.state = {
      // track which step we are on and the choices made so far
      currentStep: 0,
      userChoices : [],
      policiesShown: [], // store the policy ids we've seen so far as an array of arrays e.g., [[2,3], [3,4],...]

      // handle loading screen toggle
      loading: false,

      // toggle show Userinfo form
      showUserInfoForm: false,

      // toggle show Start page
      showStartPage: true,

      // toggle show End page,
      showEndPage: false,

      // toggle show steps
      showSteps: false,

      // toggle which loading message we show. this is used for when we are submitting final responses
      wrapup: false,

      policy_ids: [],
      policyData: [],
      policyDataSet: '',

      // form info
      userInfo: {
        username: '',
        age: '',
        race_ethnicity: '',
        gender: '',
        marital_status: '',
        education: '',
        political: '',
        positive_family: '',
        positive_anyone: '',
        healthcare_yn: '',
        healthcare_role: ''
      }
    }
    this.maxSteps = 2;
    this.uuid = uuidv4();



    // binding functions
    this.toggleUserInfoForm = this.toggleUserInfoForm.bind(this);
    this.toggleStartPage = this.toggleStartPage.bind(this);
    this.toggleEndPage = this.toggleEndPage.bind(this);
    this.updateUserInfo = this.updateUserInfo.bind(this);
    this.incrementStep = this.incrementStep.bind(this);
    this.toggleLoading = this.toggleLoading.bind(this);
    this.toggleWrapUp = this.toggleWrapUp.bind(this);
    this.updatePolicyIDs = this.updatePolicyIDs.bind(this);
    this.pushBackChoices = this.pushBackChoices.bind(this);
    this.postFinalData = this.postFinalData.bind(this);

  }


  incrementStep(){
    this.setState({
      currentStep : this.state.currentStep + 1
    }, function(){ console.log(this.state.currentStep)})
    if(this.state.currentStep === 0){
      this.toggleShowSteps();
    }
  }
  

  updatePolicyIDs(ids){
    // take the current policy_ids and push that back to policiesShown
    if(this.state.policy_ids.length > 0){
      this.state.policiesShown.push(this.state.policy_ids);
    }
    
    this.setState({
      policy_ids : ids
    })
  }

  pushBackChoices(selected){
    this.state.userChoices.push(selected);
    console.log(this.state.userChoices);
  }

  toggleShowSteps(){
    this.setState({ showSteps: !this.state.showSteps})
  }

  toggleLoading(state){
    this.setState({ loading: state})
  }

  toggleStartPage(){
    this.setState({ showStartPage: !this.state.showStartPage})
  }

  toggleEndPage(){
    this.setState({ showEndPage: !this.state.showEndPage})
  }

  toggleWrapUp(){
    this.setState({ wrapup: !this.state.wrapup})
  }

  toggleUserInfoForm(){
    this.setState({ showUserInfoForm: !this.state.showUserInfoForm})
  }

  updateUserInfo(data){
    // remove form errors messages from the object
    var toUpdate = _.omit(data, ["defaultMessage", "selectFieldMessage",
     "usernameFieldMessage", "healthcareroleFieldMessage"])

    toUpdate = Object.keys(toUpdate).reduce((obj,key) => {
          if(_.isObject(toUpdate[key])){
            obj[key] = toUpdate[key]['value']
          } else{
                obj[key] = toUpdate[key];
          }
        return obj;
      }, {})
    this.setState({
      userInfo: toUpdate
    }, 
    function(){console.log(this.state.userInfo)}
    )
  }

  postFinalData(){
    // TO-DO: add time start and time end?
    const toPostData = JSON.stringify({
      uuid: this.uuid,
      ip: this.state.ip,
      userChoices : this.state.userChoices,
      userInfo : this.state.userInfo
    })
  axios.post(`${SERVER_URL}/user_data`, toPostData,
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )
    // console.log(response)
    .then((response) =>{
      console.log(response)
    })
  }

  
  async componentDidMount() {
    
    // get IP info
    const loc_response = await fetch('https://geolocation-db.com/json/');
    const data = await loc_response.json();
    this.setState({ ip: data.IPv4 })
    // parse query string info
    const urlSearchParams = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(urlSearchParams.entries());
    // only want param mturk
    if(params['mturk']){
      this.mturk = true;
    }

    // for now we will get the first set of policies on mount
    const prevChoices = JSON.stringify({
      policiesShown: [],
      userChoices : []
    })
    const response = await axios({
      method: "POST",
      url: `${SERVER_URL}/next_query/`,
      data: prevChoices
    })
    

    this.updatePolicyIDs(response.data.policy_ids);
    console.log(response);
    console.log(this.state.policy_ids);

    const csvData = await csv(policy_data_path)
    const cleanedData = await getPolicyData(csvData);
    const datasetName = "COVID Data";
    this.setState({
      policyData: cleanedData,
      policyDataSet: datasetName
    }, function(){
      console.log(this.state.policyData);
      console.log(this.state.policyDataSet);
    })


  }
  render() {
    return(
      <React.Fragment>
        {/* <h1>Active Preference Elicitation <span role="img" aria-label="crystal ball">🔮</span> </h1> */}
        <TopNavBar/>
        <Container fluid={true} style={{marginTop : "1rem", marginBottom: "10rem"}}>
          
          <StartPage showStartPage={this.state.showStartPage}
          toggleStartPage={this.toggleStartPage}
          toggleUserInfoForm={this.toggleUserInfoForm}
          />
          <UserInfoForm showForm={this.state.showUserInfoForm}
          toggleUserInfoForm={this.toggleUserInfoForm} updateUserInfo={this.updateUserInfo}
          incrementStep={this.incrementStep} />
          {this.state.showSteps ? 
            <StepList 
              key={this.state.currentStep.toString()} // key necessary for ensuring re-render on state change
              userChoices={this.state.userChoices}
              policiesShown={this.state.policiesShown}
              maxSteps={this.maxSteps}
              policyData={this.state.policyData}
              policyDataSet={this.state.policyDataSet}
              policy_ids={this.state.policy_ids}
              currentStep={this.state.currentStep}
              loading={this.state.loading}
              wrapup={this.state.wrapup}
              incrementStep={this.incrementStep}
              toggleLoading={this.toggleLoading}
              toggleWrapUp={this.toggleWrapUp}
              toggleEndPage={this.toggleEndPage}
              updatePolicyIDs={this.updatePolicyIDs}
              postFinalData={this.postFinalData}

              userInfo={this.state.userInfo}
              ip={this.state.ip}
              uuid={this.uuid}

            /> : 
            null
          }
          <EndPage showEndPage={this.state.showEndPage}/>
        </Container>
        
        {/* <EndPage></EndPage> */}
        {/* <BottomNavBar></BottomNavBar> */}
      </React.Fragment>
    );
  }
}


export default App;

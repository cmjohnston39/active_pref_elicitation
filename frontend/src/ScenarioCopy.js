import React from 'react';
import { Col, Row } from 'reactstrap';
import PolicyDataPlot from './PolicyDataPlots';


class ScenarioCopy extends React.Component {
    constructor(props){
        super(props);
        this.key = 1;
        this.plotType="bar";
        this.maxYVal=1;
        this.columnNums = [0,6]
        this.data={
                "labels" : [
                    "Proportion of population diagnosed with COVID-19 by group_16-39",
                    "Proportion of population diagnosed with COVID-19 by group_40-49",
                    "Proportion of population diagnosed with COVID-19 by group_50-59",
                    "Proportion of population diagnosed with COVID-19 by group_60-69",
                    "Proportion of population diagnosed with COVID-19 by group_70-79",
                    "Proportion of population diagnosed with COVID-19 by group_80+"
                ],
                "values" : [
                    0.080027698,
                    0.135819567,
                    0.277178752,
                    0.294885745,
                    0.181818182,
                    0.030270056
                ]
        }

    }


    render(){
        return(
            <React.Fragment>
                <h2>Help make a difference!</h2>
                <p className="lead">
                    What happens if there aren't enough housing resources available to support each person that experiences homelessness? Who should receive these scarce resources, including permanent housing?
                </p>
                <p className="lead">
                    In 2022, approximately 580,000 individuals were experiencing homelessness in the United States. Specifically in Los Angeles, California, there were over 69,144 persons experiencing homelessness on any given night in 2022 and only 28,600 housing units for such individuals, the majority of which were already occupied. This resource shortage necessitates a way to prioritize individuals for resources as they become available. However, it is difficult to design such a policy as moral trade-offs must be made between efficiency (e.g., having the most number of individuals successfully exit homelessness) and equity (e.g., giving people resources according to their needs).
                </p>
                <p className="lead">
                    These challenges are further complicated by preexisting disparities. For example, in LA, Black people are four times more represented among those experiencing homelessness than in the general population (LAHSA 2018). Policymakers may prefer to design allocation rules that do not exacerbate inequalities, while others may prefer giving people equal chances. Allocation policies could use an individual’s <b style={{"fontWeight":'bold'}}>protected features</b>, which includes characteristics such as <b style={{"fontWeight":'bold'}}>race, gender, or age,</b> in the name of equity, or may not use these features at all, in the name of fairness.
                </p>
                <p className="lead"> Imagine that you are a policymaker deciding how to design policies that allocate scarce resources to those experiencing homelessness.
                <b style={{"fontWeight":'bold'}}>Your goal is to help determine a set of guidelines to decide who will receive housing resources, when there are more individuals in need than available resources.</b>
                </p>
                <p className="lead">
                    We have designed an adaptive questionnaire to learn your preferences for how these resources should be allocated. For each question, you will be shown a pair of policies. Please choose the policy with the features that you prefer. These features, which include information about how the policy is designed and the performance metrics of the policy if implemented, are:
                    <ol type="1">
                        <li>Number of Features Used in the Policy</li>
                        <li>Number of Protected Features Used in the Policy</li>
                        <li>Increased Likelihood of Successfully Exiting Homelessness (Overall)</li>
                        <li>Increased Likelihood of Successfully Exiting Homelessness (By Race or Ethnicity)</li>
                        <li>Increased Likelihood of Successfully Exiting Homelessness (By Gender)</li>
                        <li>Increased Likelihood of Successfully Exiting Homelessness (By Age)</li>
                    </ol> 
                </p>
                <p className="lead">
                    Features 1 and 2 are related to a policy’s level of  <b style={{"fontWeight":'bold'}}> interpretability </b>. In general, policies that use less features may be more understandable, or interpretable, to policymakers and individuals in the system. Specifically, an individual could understand why they did or did not receive a resource. However, interpretability may deteriorate the other performance metrics.               </p>
                <p className="lead">
                Features 3-6 are related to a policy’s <b style={{"fontWeight":'bold'}}> efficiency</b> (3) and <b style={{"fontWeight":'bold'}}> fairness or equity</b> (4-6), estimated using historical data for 22,165 unhoused single adults from 16 communities across the US who exited homelessness between February 2015 and April 2018. The data includes the protected information (race or ethnicity, gender, and age) of the individual and whether they 1) received a housing resource (permanent housing), or 2) self-resolved, which can include living with family. It is important to note that being unhoused is a very dynamic situation and one can return to homelessness even after receiving support. Thus, the data additionally reports whether the individual is still housed 365 days after their initial exit from homelessness, corresponding to a successful exit from homelessness.
                </p>
                <p className="lead">
                 In the graphs below, you can additionally see the proportions of the population experiencing homelessness by their race, gender, and age. Please keep this information in mind as you take the questionnaire.
                </p>
                <br></br>
                <br></br>
                {   
                    <Row className="justify-content-center" key={this.key}>
                        <Col lg={"6"} id={1} className="text-center">
                            <h4> Proportion of population diagnosed<br/>with COVID-19 by age group</h4>
                            <PolicyDataPlot key={this.key} plotType={this.plotType} data={this.data} columnNums={this.columnNums}/>
                        </Col>
                    </Row>
                    
                }
                <br></br>
                <br></br>

                <p className="lead">
                    After you select which policy you prefer, new policies are displayed to you. The questionnaire is tailored to ask questions based on your previous choices.
                </p>
                <p className="lead">
                    You can start the questionnaire by clicking on the button below. Please take the survey <b style={{"fontWeight":'bold'}}>only once</b>. 
                    Once you've started the questionnaire, <b style={{"fontWeight":'bold'}}>please do not refresh or leave the page</b>. 
                    For the questionnaire to be accepted, please take it only once and complete it in one sitting.
                    
                </p>
                <br></br>
                Sources: <br></br>
                The U.S. Department of Housing and Urban Development (2022). The 2022 Annual Homelessness Assessment Report (AHAR) to Congress. <br></br>
                LAHSA (2018) Report and Recommendations of the Ad Hoc Committee on Black People Experiencing Homelessness.

                
                
            </React.Fragment>
        )
    }
}

export default ScenarioCopy;
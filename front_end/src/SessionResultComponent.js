import React from 'react'
import './SessionResultComponent.css';


const SessionResultComponent = (props) => {
    
    return (
        <>
        <hr style={{backgroundColor:'white', height:'1px', boxShadow:'none'}}></hr>
        <div style={{ paddingBottom: '30px' }}>

            <div style={{paddingBottom: '5px'}}>
            <span style={{ fontSize: '24px', fontWeight: 'bold', textAlign: 'left', paddingRight: '20px'}}>{props.type}</span>
                <span style={{ fontSize: '24px', fontWeight: 'bold', textAlign: 'left', padding: '20px'}}>{props.instructor}</span>
                <span style={{ fontSize: '24px', fontWeight: 'bold', textAlign: 'center', padding: '20px'}}>{props.location}</span>
                <span style={{ fontSize: '24px', fontWeight: 'bold', textAlign: 'right', paddingLeft: '20px'}}>{props.start_time} to {props.end_time} on {props.days}</span>
            </div>


            <span style={{ fontSize: '24px', textAlign: 'left', paddingRight: '20px'}}>Available Spots: {props.enrollment_capacity - props.current_enrolled}/{props.enrollment_capacity}</span>
            <span style={{ fontSize: '24px', textAlign: 'left', paddingLeft: '20px'}}>Wait List Spots: {props.waitlist_capacity - props.current_waitlisted}/{props.waitlist_capacity}</span>

            </div>
            
        </>
        
      )
}




export default SessionResultComponent
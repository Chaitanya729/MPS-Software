import React from "react";
import { Link } from "react-router-dom";
const Home = () => {
    return ( 
        <div className="home">
            {/* <p>hello</p> */}
            {/* <p>home</p> */}
            <center>

             <h2>Welcome to MotorParts Shop</h2> 
            <h3>Find all your requirements near us</h3> 
            <div className="makebill_link">
                <Link to="/makebill">Makebill</Link>
            </div>
            </center>

        </div>
     );
}
 
export default Home;
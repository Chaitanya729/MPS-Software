// import { link } from 'react-router-dom/cjs/react-router-dom.min';
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom/cjs/react-router-dom';


const Makebill = () => {
    const [parts, setParts] = useState([]);
    const [error, setError] = useState(null);
    const [formData, setFormData] = useState({});
    const [loading, setloading] = useState(true)
    useEffect(() => {
        fetch('/api/parts')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch parts');
                }
                return response.json();
            })
            .then(data => {
                const initialFormData = {};
                data.forEach(part => {
                    initialFormData[part._id] = '';
                });
                setFormData(initialFormData);
                setParts(data);
                setloading(false)
            })
            .catch(error => {
                console.error('Failed to fetch parts:', error);
                setError(error.message);
            });

    }, []);

    if (loading) {
        return <div>
            <center>
            <h2> Loading... </h2>
            </center>
            </div>; 
    }


    return (
        <div className="makebill">
            <center>
            <h1>Makebill</h1>
            </center>
        
            {/* <Link>hello</Link> */}
<div className="map">
{parts.map(part => (
                    <Link to = {`/makebill/${part._id.$oid}`}>
                        <div key={part._id} className='data'>
                            <p>Weight of the component: {part.weight}</p>
                            <p>Height of the component: {part.height}</p>
                            <p>Quantity left : {part.quantity}</p>
                            <br />
                        </div>
                    </Link>
                ))}
</div>
        </div>
    );
}

export default Makebill;

import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom'
import { useHistory } from 'react-router-dom';

const Item_details = () => {
    const [temp, settemp] = useState(0)
    const {id} = useParams()
    const [part, setPart] = useState(null);
    const history = useHistory()

    useEffect(() => {
        fetch(`/api/parts/${id}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch part');
                }
                return response.json();
            })
            .then(data => setPart(data))
            .catch(error => console.error('Failed to fetch part:', error));
    }, [id]);

    if (!part) {
        return <div>Loading...</div>;
    }

    const handleClickAdd = () =>{
       if(temp<part.quantity) settemp(temp+1)
    };

    const handleClickSub = () =>{
        if(temp>=1)  settemp(temp-1)
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log("running handlesubmit")
        try {
            const response = await fetch(`/api/parts/update/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ quantity: temp }),
            });
            if (!response.ok) {
                throw new Error('Failed to update part');
            }
            console.log('Part updated successfully');
            window.location.reload(); // Reload the page

        } catch (error) {
            console.error('Failed to update part:', error);
        }
    };
    
    const handleRemove = async () => {
        try {
            const response = await fetch(`/api/parts/remove/${id}`, {
                method: 'DELETE',
            });
            if (!response.ok) {
                throw new Error('Failed to remove part');
            }
            console.log('Part removed successfully');
            history.push('/inventory');

        } catch (error) {
            console.error('Failed to remove part:', error);
        }
    };
    


    return ( 
        <div className="item_details">
            {/* <p>hello there</p> */}
            <p>weight = {part.weight}</p>
            <p>height = {part.height}</p>
            <p>quantity left  = {part.quantity}</p>
            <button  onClick={handleClickAdd}>+</button>
            {temp}
            <button onClick={handleClickSub}>-</button>
            <h2> hello - {part.weight}</h2>
            <button onClick={handleSubmit}>Submit</button>
            <button onClick={handleRemove}>Remove Item</button>

        </div>
     );
}
 
export default Item_details;
import React, { useState } from "react";
import { useHistory } from "react-router-dom"; 

const Add_items = () => {
    const [name, setName] = useState('')
    const [weight, setWeight] = useState(0);
    const [height, setHeight] = useState(0);
    const [quantity, setQuantity] = useState(0);
    const [image, setImage] = useState(null)
    const [price, setPrice] = useState(0)
    const [errorMessage, setErrorMessage] = useState('');

    const history = useHistory()

    const handleNameChange = (e) => {
        setName(e.target.value)
    }

    const handleWeightChange = (e) => {
        setWeight(e.target.value);
    }

    const handleHeightChange = (e) => {
        setHeight(e.target.value);
    }
    
    const handleQuantityChange = (e) => {
        setQuantity(e.target.value);
    }

    const handlePriceChange = (e) => {
        setPrice(e.target.value)
    }
    
    const handleImageChange = async(e) => {
        if (e.target.files && e.target.files.length > 0) {
            setImage(e.target.files[0]);
        } else {
            console.log('No file selected');
        }
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!weight  || !height  || !quantity || !price || !name) {
            setErrorMessage('All fields are required');
            return;
        }

        const formData = new FormData();
        formData.append('name', name)
        formData.append('weight', weight)
        formData.append('height', height)
        formData.append('quantity', quantity)
        formData.append('image', image)
        formData.append('price', price)
        formData.append('status',0)

        try {
            const response = await fetch('/api/add_item', {
                method: 'POST',
                body: formData, // Send the form data
            });
            if (!response.ok) {
                throw new Error('Failed to add item');
            }
            history.push('/inventory');
            console.log('Item added successfully');
        } catch (error) {
            console.error('Failed to add item:', error);
        }
    };
    
    
    return ( 
        <div className="add_items">
            <p>Add items</p>
            <form onSubmit={handleSubmit}>
                <div className="enter">
                    <p>Name</p>
                    <input type = "text" onChange={handleNameChange} />
                </div>

               <div className="enter">
                    <p>Weight</p>
                    <input type="number"  onChange={handleWeightChange} />
               </div>
               
               <div className="enter">
                    <p>Height</p>
                    <input type="number"  onChange={handleHeightChange} />
               </div>

               <div className="enter">
                    <p>Quantity</p>
                    <input type="number"  onChange={handleQuantityChange} />
               </div>

               <div className="enter">
                <p>Price ($) </p>
                <input type="number" onChange={handlePriceChange} />
               </div>

               <div className="enter">
                    <p>Image</p>
                    <input type="file" onChange={handleImageChange} />
               </div> 

               <div className="submit">
                    <button type="submit">Submit</button>
               </div>
            </form>
        </div>
    );
};

export default Add_items;


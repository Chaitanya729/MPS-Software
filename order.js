import React, {useState, useEffect} from 'react'
import { useHistory } from 'react-router-dom'
import axios from 'axios'

const Order = () => {

    const [orders,setOrders] = useState([])
    const [error, setError] = useState(null)
    const history = useHistory()
    const [searchOrder, setSearchOrder] = useState('')

    const handleOrderGeneration = async () => {
        const response = await axios.get('http://localhost:5000/order/sendorder')
    }

    useEffect(() => {
        const fetchParts = async () => {
            try {
                const response = await fetch('/api/orders');
                if (!response.ok) {
                    throw new Error('Failed to fetch parts');
                }
                const data = await response.json();
                setOrders(data.map((part, index) => ({ ...part, index: index + 1 }))); // Add an index to each part
            } catch (error) {
                console.error('Failed to fetch parts:', error);
                setError(error.message);
            }
        };
        fetchParts();

        return () => {}
    }, []);

    return ( 
        <div className="inventory">
            <div className="parts-list">
                {orders.length > 0 ? orders.map((part, index) => (
                    <div key={part._id.$oid} className="part-item">
                        <img src={`data:image/jpeg;base64,${part.image}`} alt="Part" className="part-image" />
                        <div className="part-details">
                            <h3>{index + 1}. {part.name}</h3>
                            <p>ID: {part._id.$oid}</p>
                            <p>Quantity: {part.quantity}</p>
                        </div>
                        <div className="part-price">
                            <p>${part.price}</p>
                        </div>
                    </div>
                )) : <div className="loading-message">Loading...</div>}
            </div>
            <button onClick={handleOrderGeneration}>Order Items</button>
        </div>
     );
}
 
export default Order;
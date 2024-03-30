import React, {useState, useEffect} from 'react'
import { useHistory } from 'react-router-dom'
import axios from 'axios'

const Inventory = () => {

    const [parts, setParts] = useState([])
    const [error,setError] = useState(null)
    const history = useHistory()
    const [searchTerm, setSearchTerm] = useState('')

    const handleClick = () =>{
        history.push('/add_items')
    }

    const handleSearch = async () => {
        const response = await axios.get(`/api/search?query=${searchTerm}`)
        console.log(response.data.length)
        console.log(response.data)
        setParts(response.data)
    }

    useEffect(() => {
        const fetchParts = async () => {
            try {
                const url = searchTerm ? `/api/search?query=${searchTerm}` : '/api/parts'
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error('Failed to fetch parts');
                }
                const data = await response.json();
                setParts(data.map((part, index) => ({ ...part, index: index + 1 }))); // Add an index to each part
            } catch (error) {
                console.error('Failed to fetch parts:', error);
                setError(error.message);
            }
        };
        fetchParts();
    }, [searchTerm]);

    if(error) return <div>Error : { error }</div>

    return ( 
        <div className="inventory">
            <div className="search-bar">
                <input 
                    type="text"
                    placeholder='Search'
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                />
                <button onClick={handleSearch}>Search</button>
            </div>
            <div className="parts-list">
                {parts.length > 0 ? parts.map((part, index) => (
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
            <div className="add-item-section">
                <p>Want to add some items into your inventory?</p>
                <button onClick={handleClick}>Click Here</button>
            </div>
        </div>
    );
}
 
export default Inventory;
import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000/api/items'

function ItemList() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    quantity: ''
  })

  useEffect(() => {
    fetchItems()
  }, [])

  const fetchItems = async () => {
    try {
      setLoading(true)
      const response = await axios.get(API_URL)
      setItems(response.data)
      setError(null)
    } catch (err) {
      setError('Failed to fetch items')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await axios.post(API_URL, {
        name: formData.name,
        description: formData.description,
        price: parseFloat(formData.price),
        quantity: parseInt(formData.quantity)
      })
      setFormData({ name: '', description: '', price: '', quantity: '' })
      fetchItems()
    } catch (err) {
      setError('Failed to create item')
      console.error(err)
    }
  }

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${API_URL}/${id}`)
      fetchItems()
    } catch (err) {
      setError('Failed to delete item')
      console.error(err)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  if (loading) return Loading...
  if (error) return {error}

  return (
    
      Create New Item
      
        
          
          
        
        
          
          
          
            Add Item
          
        
      

      Items
      
        {items.length === 0 ? (
          No items found. Create one above!
        ) : (
          items.map((item) => (
            
              {item.name}
              {item.description || 'No description'}
              Price: ${item.price.toFixed(2)}
              Quantity: {item.quantity}
              <button
                onClick={() => handleDelete(item._id)}
                style={{
                  padding: '5px 10px',
                  backgroundColor: '#ff4444',
                  color: 'white',
                  border: 'none',
                  borderRadius: '3px',
                  cursor: 'pointer'
                }}
              >
                Delete
              
            
          ))
        )}
      
    
  )
}

export default ItemList
import React from 'react'
import OrderbookColumn from './Column'

import './Orderbook.css'

class Orderbook extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      count: 90
    }
  }

  render() {
    return (
      <div className='orderbook-container'>
          <OrderbookColumn
            name={'BIDS'}
          />
          <OrderbookColumn
            name={'ASKS'}
          />
      </div>
    )
  }
}

export default Orderbook
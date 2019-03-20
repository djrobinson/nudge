import React from 'react'

import OrderbookCell from './Cell'

const OrderbookColumn = ({name}) => (
    <container className="ob-col">
        <row>
            <h3>{name}</h3>
        </row>
        <row>
            <OrderbookCell
                name={"ejlkjs"}
            />
        </row>
    </container>
);

export default OrderbookColumn
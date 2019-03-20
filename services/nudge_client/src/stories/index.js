import React from 'react';

import { storiesOf } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import { linkTo } from '@storybook/addon-links';

import TestSocket from '../components/TestSocket';

import Orderbook from '../components/Orderbook/Orderbook';


storiesOf('Button', module)
  .add('with text', () => <TestSocket onClick={action('clicked')}>Hello Button</TestSocket>)
  .add('with some emoji', () => (
    <h1>Test</h1>
  ));

storiesOf('OrderBook', module)
  .add('with text', () => <Orderbook />)
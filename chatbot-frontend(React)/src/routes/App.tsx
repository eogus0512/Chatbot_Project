import * as React from 'react';
import { Route, Switch, Router } from 'react-router-dom';
import { BrowserRouter } from 'react-router-dom';
import { HomePage } from "../pages";

const Root: React.FC = () => (
  // TODO 루트 라우터를 반환
  <BrowserRouter>
    <Switch>
      <Route path="/" exact component={HomePage} />
    </Switch>
  </BrowserRouter>
)

export default Root;
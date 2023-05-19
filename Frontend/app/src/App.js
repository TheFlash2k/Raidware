import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Components/Login';
import Register from './Components/Register';
import Dashboard from './Components/Dashboard';
import Logout from './Components/Logout';
import Listeners from './Components/Listeners';
import Users from './Components/Users';
import Loot from './Components/Loot';
import Session from './Components/Sessions';
import Agent from './Components/Agent';
import { useState } from 'react';

function requireAuth(nextState, replace, next) {
  console.log("Token: " + localStorage.getItem("token"));
  if (!localStorage.getItem("token")) {
    replace({
      pathname: "/login",
      state: { nextPathname: nextState.location.pathname }
    });
  }
  next();
}

function App() {

  const [theme, setTheme] = useState('light');

  return (
   <Router>
      <Routes>
        <Route path="/login" Component={Login} />
        <Route path="/register" Component={Register} />
        <Route path="/dashboard" Component={Dashboard} />
        <Route path="/" Component={Dashboard} />
        <Route path="/listeners" Component={Listeners} onEnter={requireAuth}   />
        <Route path="/users" element={<Users/>} onEnter={requireAuth}  />
        <Route path="/loot" element={<Loot onEnter={requireAuth}/>} />
        <Route path = "/sessions" element={<Session theme={theme} setTheme={setTheme} />} />
        <Route path = "/logout" Component={Logout} />
        <Route path = "/agents" Component={Agent} />
      </Routes>
    </Router>
    
  );
}

export default App;

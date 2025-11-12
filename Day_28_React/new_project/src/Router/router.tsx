import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import HomePage from '../pages/home/HomePage';
import LoginPage from '../pages/login/LoginPage';
import Layout from './Layout';

export default function Router() {
  return (
    <>
      <BrowserRouter>
        <Routes>
            <Route path = "" element={<Layout/>} >
                <Route path = "" element={<HomePage/>} />
                <Route path = "login" element = {<LoginPage/>} />
            </Route>
        </Routes>
      
      
      
      </BrowserRouter>
    </>
  )
}



import React from 'react'
import Footer from '../components/footer/Footer'
import NavBar from '../components/navbar/NavBar'
import { Outlet } from 'react-router-dom'


export default function Layout() {
  return (
    <>
      <NavBar/>
         <Outlet/>
      <Footer/>
    </>
  )
}

import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, CalendarDays, Users, BookOpen, UserPlus } from 'lucide-react';
import './Navbar.css';
import ibadLogo from '../assets/ibad-logo.png';

const Navbar = () => {
  return (
    <nav className="navbar glass-panel">
      <NavLink to="/" className="nav-brand">
        <img src={ibadLogo} alt="IBAD Akademi Logo" className="brand-logo-img" />
        <div className="brand-text-group">
          <span className="brand-text">IBAD Akademi</span>
          <span className="brand-sub">Internationale Bildungsakademie</span>
        </div>
      </NavLink>
      <ul className="nav-links">
        <li>
          <NavLink to="/" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <Home size={18} />
            <span>Ana Sayfa</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/program" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <CalendarDays size={18} />
            <span>Program</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/kadro" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <Users size={18} />
            <span>Kadro</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/dersler" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <BookOpen size={18} />
            <span>Dersler</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/basvuru" className={({ isActive }) => isActive ? "nav-link active application-btn" : "nav-link application-btn"}>
            <UserPlus size={18} />
            <span>Başvuru</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/admin" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <span style={{fontSize: "1.2rem"}}>⚙️</span>
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;

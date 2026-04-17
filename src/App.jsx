import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Courses from './pages/Courses';
import Application from './pages/Application';
import Admin from './pages/Admin';
import TeacherCard from './components/TeacherCard';
import ScheduleTable from './components/ScheduleTable';
import teachersData from './data/teachers.json';
import scheduleData from './data/schedule.json';

const TeachersPage = () => (
  <div className="grid-container fade-in-up">
    {teachersData.map((teacher, index) => (
      <TeacherCard 
        key={index} 
        teacher={teacher} 
        delay={index * 0.1} 
      />
    ))}
  </div>
);

const SchedulePage = () => (
  <div className="fade-in-up">
    <ScheduleTable schedule={scheduleData} />
  </div>
);

function App() {
  return (
    <Router basename="/akademi">
      <div className="container">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/program" element={<SchedulePage />} />
            <Route path="/kadro" element={<TeachersPage />} />
            <Route path="/dersler" element={<Courses />} />
            <Route path="/basvuru" element={<Application />} />
            <Route path="/admin" element={<Admin />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

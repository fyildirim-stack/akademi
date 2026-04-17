import React from 'react';
import { User, BookOpen, Clock } from 'lucide-react';
import './TeacherCard.css';

const TeacherCard = ({ teacher, delay }) => {
  return (
    <div className="teacher-card glass-panel fade-in-up" style={{ animationDelay: `${delay}s` }}>
      <div className="teacher-header">
        <div className="avatar-placeholder">
          <User size={32} />
        </div>
        <div>
          <h3>{teacher.name}</h3>
          <span className="badge">{teacher.field}</span>
        </div>
      </div>
      
      <div className="teacher-body">
        <div className="info-row">
          <BookOpen size={18} className="icon" />
          <span>{teacher.course}</span>
        </div>
        <div className="info-row">
          <Clock size={18} className="icon" />
          <span>Toplam {teacher.total_hours} Saat</span>
        </div>
      </div>
    </div>
  );
};

export default TeacherCard;

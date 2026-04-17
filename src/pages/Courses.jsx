import React from 'react';
import './Courses.css';
import { Book, Clock, GraduationCap } from 'lucide-react';
import teachersData from '../data/teachers.json';

const Courses = () => {
  return (
    <div className="courses-container fade-in-up">
      <div className="page-header">
        <h1>Dersler ve İçerikleri</h1>
        <p>Akademimizdeki tüm derslerin detayları ve eğitim hedefleri.</p>
      </div>

      <div className="courses-grid">
        {teachersData.map((t, index) => (
          <div key={index} className="course-card glass-panel">
            <div className="course-card-header">
              <span className="course-field-badge">{t.field}</span>
              <h2 className="course-title">{t.course}</h2>
            </div>
            
            <div className="course-card-body">
              <p className="course-description">
                Bu ders {t.field} alanında katılımcılara derinlemesine bir bakış açısı sunmayı amaçlamaktadır. 
                Ders kapsamında {t.course} konuları akademik bir titizlikle işlenecek olup, teorik bilginin yanı 
                sıra güncel meseleler de tartışılacaktır.
              </p>
              
              <div className="course-meta">
                <div className="meta-item">
                  <GraduationCap size={18} className="meta-icon" />
                  <span>{t.name}</span>
                </div>
                <div className="meta-item">
                  <Clock size={18} className="meta-icon" />
                  <span>Toplam {t.total_hours} Hafta (40 Saat)</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Courses;

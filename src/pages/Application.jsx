import React, { useState } from 'react';
import './Application.css';
import { Send, CheckCircle } from 'lucide-react';

const Application = () => {
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    university: '',
    department: '',
    motivation: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Save to localStorage
    const savedApps = JSON.parse(localStorage.getItem('akademi_applications') || '[]');
    const newApp = {
      id: Date.now().toString(),
      ...formData,
      status: 'pending',
      date: new Date().toLocaleDateString('tr-TR')
    };
    
    localStorage.setItem('akademi_applications', JSON.stringify([newApp, ...savedApps]));

    setTimeout(() => {
      setSubmitted(true);
      setFormData({
        firstName: '', lastName: '', email: '', phone: '',
        university: '', department: '', motivation: ''
      });
    }, 500);
  };

  if (submitted) {
    return (
      <div className="application-container fade-in-up">
        <div className="success-card glass-panel">
          <CheckCircle size={64} className="success-icon" />
          <h2>Başvurunuz Alındı!</h2>
          <p>
            Akademi programımıza göstermiş olduğunuz ilgi için teşekkür ederiz. 
            Başvurunuz değerlendirme komitesine iletilmiştir. Sonuçlar e-posta 
            adresinize bildirilecektir.
          </p>
          <button className="btn btn-primary" onClick={() => setSubmitted(false)}>
            Yeni Başvuru Yap
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="application-container fade-in-up">
      <div className="page-header">
        <h1>Akademi Başvuru Formu</h1>
        <p>2026-2027 Eğitim Dönemi için ön başvurunuzu oluşturun.</p>
      </div>

      <div className="form-wrapper glass-panel">
        <form className="application-form" onSubmit={handleSubmit}>
          
          <div className="form-section">
            <h3>Kişisel Bilgiler</h3>
            <div className="form-row">
              <div className="form-group">
                <label>Adınız</label>
                <input type="text" name="firstName" value={formData.firstName} onChange={handleChange} required placeholder="Adınız" />
              </div>
              <div className="form-group">
                <label>Soyadınız</label>
                <input type="text" name="lastName" value={formData.lastName} onChange={handleChange} required placeholder="Soyadınız" />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>E-Posta Adresiniz</label>
                <input type="email" name="email" value={formData.email} onChange={handleChange} required placeholder="ornek@email.com" />
              </div>
              <div className="form-group">
                <label>Telefon Numaranız</label>
                <input type="tel" name="phone" value={formData.phone} onChange={handleChange} required placeholder="05XX XXX XX XX" />
              </div>
            </div>
          </div>

          <div className="form-section">
            <h3>Eğitim Bilgileri</h3>
            <div className="form-row">
              <div className="form-group">
                <label>Üniversite</label>
                <input type="text" name="university" value={formData.university} onChange={handleChange} required placeholder="Mezun olduğunuz/Okuduğunuz Üniversite" />
              </div>
              <div className="form-group">
                <label>Bölüm</label>
                <input type="text" name="department" value={formData.department} onChange={handleChange} required placeholder="Bölümünüz" />
              </div>
            </div>
          </div>

          <div className="form-section">
            <h3>Başvuru Detayları</h3>
            <div className="form-group full-width">
              <label>Neden Akademimize Katılmak İstiyorsunuz?</label>
              <textarea name="motivation" value={formData.motivation} onChange={handleChange} required rows="5" placeholder="Lütfen motivasyonunuzu kısaca açıklayınız..."></textarea>
            </div>
            
            <div className="form-group full-width checkbox-group">
              <input type="checkbox" id="terms" required />
              <label htmlFor="terms">Hafta sonu Cumartesi ve Pazar günleri tam zamanlı katılım sağlayacağımı taahhüt ederim.</label>
            </div>
          </div>

          <button type="submit" className="submit-btn btn btn-primary">
            <Send size={18} />
            Başvuruyu Tamamla
          </button>
        </form>
      </div>
    </div>
  );
};

export default Application;

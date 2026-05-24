import React from 'react';
import './Home.css';
import { BookOpen, Users, CalendarDays, Award } from 'lucide-react';
import { Link } from 'react-router-dom';
import heroBanner from '../assets/hero-banner.png';

const Home = () => {
  return (
    <div className="home-container fade-in-up">
      <div className="hero-section glass-panel" style={{backgroundImage: `url(${heroBanner})`}}>
        <div className="hero-logo-area">
          <img src="/akademi/assets/ibad-logo.png" alt="IBAD Akademi" className="hero-logo" onError={(e) => e.target.style.display='none'} />
        </div>
        <h1>İlmi Derinlik, Fikri Öncülük</h1>
        <p className="hero-tagline">Internationale Bildungsakademie Deutschland e.V.</p>
        <p className="hero-subtitle">
          IBAD Akademi, Almanya'da yaşayan Türkçe konuşan topluluklar için 
          İlahiyat, İktisat, Hukuk ve Sosyal Bilimler alanlarında akademik 
          düzeyde hafta sonu eğitim programları sunan bir eğitim akademisidir.
        </p>
        <div className="hero-actions">
          <Link to="/basvuru" className="btn btn-primary">Hemen Başvur</Link>
          <Link to="/program" className="btn btn-secondary">Programı İncele</Link>
        </div>
      </div>

      <div className="features-grid">
        <div className="feature-card glass-panel">
          <div className="feature-icon"><Users size={32} /></div>
          <h3>Uzman Kadro</h3>
          <p>Alanında otorite olan akademisyenler ve profesyonellerden eğitim alın.</p>
        </div>
        
        <div className="feature-card glass-panel">
          <div className="feature-icon"><BookOpen size={32} /></div>
          <h3>Zengin İçerik</h3>
          <p>İlahiyattan iktisada, siyasi tarihten sosyolojiye geniş bir müfredat.</p>
        </div>

        <div className="feature-card glass-panel">
          <div className="feature-icon"><CalendarDays size={32} /></div>
          <h3>Hafta Sonu Eğitimi</h3>
          <p>Çalışanlar ve öğrenciler için optimize edilmiş Cumartesi-Pazar programı.</p>
        </div>

        <div className="feature-card glass-panel">
          <div className="feature-icon"><Award size={32} /></div>
          <h3>Sertifika</h3>
          <p>Eğitimi başarıyla tamamlayan tüm katılımcılara katılım belgesi ve sertifika.</p>
        </div>
      </div>

      <div className="about-section glass-panel">
        <h2>IBAD Akademi Hakkında</h2>
        <p>
          <strong>Internationale Bildungsakademie Deutschland e.V. (IBAD)</strong>, 
          Almanya'da kurulan bağımsız bir eğitim derneğidir. Akademimiz; İslami ilimler, iktisat, hukuk 
          ve sosyal bilimler gibi farklı disiplinlerde akademik düzeyde eğitimler 
          sunmayı hedeflemektedir.
        </p>
        <p>
          40'tan fazla haftalık yoğun programımız boyunca öğrencilerimiz sadece teorik 
          bilgi almakla kalmayacak; alanının önde gelen isimleriyle interaktif tartışma 
          ortamlarında bulunma ve kendi fikirlerini geliştirme fırsatı yakalayacaklardır.
        </p>
      </div>
    </div>
  );
};

export default Home;

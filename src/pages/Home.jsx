import React from 'react';
import './Home.css';
import { BookOpen, Users, CalendarDays, Award } from 'lucide-react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="home-container fade-in-up">
      <div className="hero-section glass-panel">
        <h1>İlmi Derinlik, Fikri Öncülük</h1>
        <p className="hero-subtitle">
          Hafta sonu akademik çalışma programımız ile alanında uzman akademisyenlerden 
          eğitim alma fırsatını yakalayın. İktisat, İlahiyat, Hukuk ve daha birçok alanda 
          derinlemesine bilgi edinin.
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
        <h2>Akademi Hakkında</h2>
        <p>
          Akademimiz, farklı disiplinlerde bilgi sahibi olmak isteyen, akademik vizyonunu 
          genişletmeyi hedefleyen ve topluma yön verecek liderler yetiştirmeyi amaçlayan 
          bir eğitim inisiyatifidir. Modern çağın gereksinimleri ile geleneksel bilgeliği 
          harmanlayarak katılımcılara eşsiz bir öğrenme deneyimi sunuyoruz.
        </p>
        <p>
          44 haftalık yoğun programımız boyunca öğrencilerimiz sadece teorik bilgi almakla 
          kalmayacak, aynı zamanda alanının önde gelen isimleriyle interaktif tartışma 
          ortamlarında bulunma fırsatı yakalayacaklardır.
        </p>
      </div>
    </div>
  );
};

export default Home;

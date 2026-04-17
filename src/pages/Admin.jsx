import React, { useState, useEffect } from 'react';
import './Admin.css';
import { UserCheck, UserX, Trash2, Search, Filter } from 'lucide-react';

const Admin = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return sessionStorage.getItem('akademi_admin_auth') === 'true';
  });
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState('');

  const [applications, setApplications] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    if (isAuthenticated) {
      const savedApps = JSON.parse(localStorage.getItem('akademi_applications') || '[]');
      setApplications(savedApps);
    }
  }, [isAuthenticated]);

  const saveApplications = (updatedApps) => {
    setApplications(updatedApps);
    localStorage.setItem('akademi_applications', JSON.stringify(updatedApps));
  };

  const handleLogin = (e) => {
    e.preventDefault();
    // Basit bir ön yüz doğrulaması
    if (username === 'admin' && password === 'akademi2026') {
      sessionStorage.setItem('akademi_admin_auth', 'true');
      setIsAuthenticated(true);
      setLoginError('');
    } else {
      setLoginError('Kullanıcı adı veya şifre hatalı!');
    }
  };

  const handleLogout = () => {
    sessionStorage.removeItem('akademi_admin_auth');
    setIsAuthenticated(false);
    setUsername('');
    setPassword('');
  };

  const handleStatusChange = (id, newStatus) => {
    const updated = applications.map(app => 
      app.id === id ? { ...app, status: newStatus } : app
    );
    saveApplications(updated);
  };

  const handleDelete = (id) => {
    if(window.confirm('Bu başvuruyu silmek istediğinize emin misiniz?')) {
      const updated = applications.filter(app => app.id !== id);
      saveApplications(updated);
    }
  };

  const filteredApps = applications.filter(app => 
    `${app.firstName} ${app.lastName}`.toLowerCase().includes(searchTerm.toLowerCase()) ||
    app.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    app.university.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusBadge = (status) => {
    switch(status) {
      case 'approved': return <span className="status-badge approved">Onaylandı</span>;
      case 'rejected': return <span className="status-badge rejected">Reddedildi</span>;
      default: return <span className="status-badge pending">Beklemede</span>;
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="admin-login-container fade-in-up">
        <div className="login-card glass-panel">
          <div className="login-header">
            <span style={{fontSize: '3rem', marginBottom: '1rem', display: 'block'}}>🔒</span>
            <h2>Yönetici Girişi</h2>
            <p>Panele erişmek için yetkili bilgilerini giriniz.</p>
          </div>
          <form onSubmit={handleLogin} className="login-form">
            {loginError && <div className="error-message">{loginError}</div>}
            <div className="form-group">
              <label>Kullanıcı Adı</label>
              <input 
                type="text" 
                value={username} 
                onChange={(e) => setUsername(e.target.value)} 
                required 
                placeholder="Kullanıcı adınızı girin"
              />
            </div>
            <div className="form-group">
              <label>Parola</label>
              <input 
                type="password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)} 
                required 
                placeholder="Parolanızı girin"
              />
            </div>
            <button type="submit" className="btn btn-primary login-btn">
              Giriş Yap
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-container fade-in-up">
      <div className="admin-header glass-panel">
        <div className="admin-header-left">
          <h1>Başvuru Yönetim Paneli</h1>
          <p>Adayların başvurularını inceleyin, onaylayın veya reddedin.</p>
        </div>
        <div className="admin-stats">
          <div className="stat-box">
            <span className="stat-num">{applications.length}</span>
            <span className="stat-label">Toplam</span>
          </div>
          <div className="stat-box">
            <span className="stat-num approved-text">
              {applications.filter(a => a.status === 'approved').length}
            </span>
            <span className="stat-label">Onaylanan</span>
          </div>
          <button className="btn btn-secondary logout-btn" onClick={handleLogout} title="Çıkış Yap">
            <UserX size={18} /> Çıkış
          </button>
        </div>
      </div>

      <div className="admin-controls glass-panel">
        <div className="search-box">
          <Search size={18} className="search-icon" />
          <input 
            type="text" 
            placeholder="İsim, e-posta veya üniversite ara..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <button className="btn btn-secondary filter-btn">
          <Filter size={18} /> Filtrele
        </button>
      </div>

      <div className="applications-table-wrapper glass-panel">
        {filteredApps.length === 0 ? (
          <div className="empty-state">
            <p>Henüz gösterilecek bir başvuru bulunmuyor.</p>
          </div>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>Aday Bilgileri</th>
                <th>Eğitim Bilgileri</th>
                <th>Motivasyon & Tarih</th>
                <th>Durum</th>
                <th>İşlemler</th>
              </tr>
            </thead>
            <tbody>
              {filteredApps.map(app => (
                <tr key={app.id}>
                  <td>
                    <div className="applicant-info">
                      <strong>{app.firstName} {app.lastName}</strong>
                      <span className="info-sub">{app.email}</span>
                      <span className="info-sub">{app.phone}</span>
                    </div>
                  </td>
                  <td>
                    <div className="applicant-info">
                      <strong>{app.university}</strong>
                      <span className="info-sub">{app.department}</span>
                    </div>
                  </td>
                  <td>
                    <div className="motivation-text" title={app.motivation}>
                      {app.motivation.length > 50 ? app.motivation.substring(0, 50) + '...' : app.motivation}
                    </div>
                    <span className="info-sub date-text">{app.date}</span>
                  </td>
                  <td>
                    {getStatusBadge(app.status)}
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button 
                        className={`action-btn approve ${app.status === 'approved' ? 'active' : ''}`}
                        onClick={() => handleStatusChange(app.id, 'approved')}
                        title="Onayla"
                      >
                        <UserCheck size={16} />
                      </button>
                      <button 
                        className={`action-btn reject ${app.status === 'rejected' ? 'active' : ''}`}
                        onClick={() => handleStatusChange(app.id, 'rejected')}
                        title="Reddet"
                      >
                        <UserX size={16} />
                      </button>
                      <button 
                        className="action-btn delete"
                        onClick={() => handleDelete(app.id)}
                        title="Sil"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Admin;

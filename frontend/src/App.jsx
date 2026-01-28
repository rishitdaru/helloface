import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import Home from './pages/Home';
import Enroll from './pages/Enroll';
import Recognize from './pages/Recognize';
import Users from './pages/Users';
import './styles/index.css';

const Navigation = () => {
    const location = useLocation();

    const isActive = (path) => {
        return location.pathname === path;
    };

    return (
        <nav style={{
            background: 'var(--color-bg-secondary)',
            borderBottom: '1px solid var(--glass-border)',
            padding: '1rem 0',
            position: 'sticky',
            top: 0,
            zIndex: 100,
            backdropFilter: 'blur(10px)',
            WebkitBackdropFilter: 'blur(10px)'
        }}>
            <div className="container" style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                flexWrap: 'wrap',
                gap: '1rem'
            }}>
                <Link to="/" style={{ textDecoration: 'none' }}>
                    <h2 style={{
                        margin: 0,
                        fontSize: '1.5rem',
                        background: 'var(--gradient-primary)',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        backgroundClip: 'text'
                    }}>
                        👋 HelloFace
                    </h2>
                </Link>

                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                    <Link to="/" style={{ textDecoration: 'none' }}>
                        <button className={isActive('/') ? 'btn btn-primary' : 'btn btn-secondary'}>
                            🏠 Home
                        </button>
                    </Link>
                    <Link to="/enroll" style={{ textDecoration: 'none' }}>
                        <button className={isActive('/enroll') ? 'btn btn-primary' : 'btn btn-secondary'}>
                            👤 Enroll
                        </button>
                    </Link>
                    <Link to="/recognize" style={{ textDecoration: 'none' }}>
                        <button className={isActive('/recognize') ? 'btn btn-primary' : 'btn btn-secondary'}>
                            🔍 Recognize
                        </button>
                    </Link>
                    <Link to="/users" style={{ textDecoration: 'none' }}>
                        <button className={isActive('/users') ? 'btn btn-primary' : 'btn btn-secondary'}>
                            👥 Users
                        </button>
                    </Link>
                </div>
            </div>
        </nav>
    );
};

const App = () => {
    return (
        <Router>
            <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
                <Navigation />
                <main style={{ flex: 1 }}>
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/enroll" element={<Enroll />} />
                        <Route path="/recognize" element={<Recognize />} />
                        <Route path="/users" element={<Users />} />
                    </Routes>
                </main>
                <footer style={{
                    background: 'var(--color-bg-secondary)',
                    borderTop: '1px solid var(--glass-border)',
                    padding: '2rem 0',
                    marginTop: '4rem'
                }}>
                    <div className="container text-center">
                        <p style={{ color: 'var(--color-text-muted)', margin: 0 }}>
                            HelloFace - 100% Free, Open-Source Face Recognition
                        </p>
                        <p style={{ color: 'var(--color-text-muted)', margin: '0.5rem 0 0 0', fontSize: '0.9rem' }}>
                            Built with ❤️ using MediaPipe, InsightFace, FAISS, FastAPI & React
                        </p>
                    </div>
                </footer>
            </div>
        </Router>
    );
};

export default App;

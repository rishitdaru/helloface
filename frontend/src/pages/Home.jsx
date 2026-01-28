import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api';

const Home = () => {
    const [stats, setStats] = useState(null);
    const [health, setHealth] = useState(null);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [statsData, healthData] = await Promise.all([
                api.getStats(),
                api.healthCheck()
            ]);
            setStats(statsData);
            setHealth(healthData);
        } catch (error) {
            console.error('Failed to fetch data:', error);
        }
    };

    return (
        <div className="container" style={{ padding: '2rem 1rem' }}>
            {/* Hero Section */}
            <div className="text-center mb-2">
                <h1 style={{
                    fontSize: '3.5rem',
                    background: 'var(--gradient-primary)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text',
                    marginBottom: '1rem'
                }}>
                    👋 HelloFace
                </h1>
                <p style={{ fontSize: '1.25rem', color: 'var(--color-text-secondary)', maxWidth: '600px', margin: '0 auto' }}>
                    100% Free, Open-Source Face Recognition System
                </p>
                <p style={{ color: 'var(--color-text-muted)', marginTop: '0.5rem' }}>
                    No API Keys • No External Services • Fully Local
                </p>
            </div>

            {/* Status Card */}
            {health && (
                <div className="glass-card mb-2">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', justifyContent: 'center' }}>
                        <div style={{
                            width: '12px',
                            height: '12px',
                            borderRadius: '50%',
                            background: health.status === 'healthy' ? 'var(--color-success)' : 'var(--color-danger)',
                            boxShadow: `0 0 10px ${health.status === 'healthy' ? 'var(--color-success)' : 'var(--color-danger)'}`
                        }}></div>
                        <span style={{ fontWeight: 500 }}>
                            System Status: {health.status === 'healthy' ? '✅ Healthy' : '❌ Unhealthy'}
                        </span>
                    </div>
                </div>
            )}

            {/* Stats */}
            {stats && (
                <div className="grid grid-2 mb-2">
                    <div className="glass-card text-center">
                        <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>👥</div>
                        <h3 style={{ fontSize: '2.5rem', margin: 0 }}>{stats.total_users}</h3>
                        <p style={{ color: 'var(--color-text-muted)', margin: 0 }}>Enrolled Users</p>
                    </div>
                    <div className="glass-card text-center">
                        <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>🎯</div>
                        <h3 style={{ fontSize: '2.5rem', margin: 0 }}>{(stats.recognition_threshold * 100).toFixed(0)}%</h3>
                        <p style={{ color: 'var(--color-text-muted)', margin: 0 }}>Recognition Threshold</p>
                    </div>
                </div>
            )}

            {/* Action Cards */}
            <div className="grid grid-2 mb-2">
                <Link to="/enroll" style={{ textDecoration: 'none' }}>
                    <div className="glass-card" style={{ cursor: 'pointer', height: '100%' }}>
                        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>👤</div>
                        <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Enroll User</h3>
                        <p style={{ color: 'var(--color-text-secondary)', margin: 0 }}>
                            Register a new face in the system
                        </p>
                    </div>
                </Link>

                <Link to="/recognize" style={{ textDecoration: 'none' }}>
                    <div className="glass-card" style={{ cursor: 'pointer', height: '100%' }}>
                        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🔍</div>
                        <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Recognize Face</h3>
                        <p style={{ color: 'var(--color-text-secondary)', margin: 0 }}>
                            Identify enrolled users in real-time
                        </p>
                    </div>
                </Link>

                <Link to="/users" style={{ textDecoration: 'none' }}>
                    <div className="glass-card" style={{ cursor: 'pointer', height: '100%' }}>
                        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📋</div>
                        <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Manage Users</h3>
                        <p style={{ color: 'var(--color-text-secondary)', margin: 0 }}>
                            View and manage all enrolled users
                        </p>
                    </div>
                </Link>

                <div className="glass-card" style={{ height: '100%' }}>
                    <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>⚙️</div>
                    <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Features</h3>
                    <ul style={{ color: 'var(--color-text-secondary)', paddingLeft: '1.25rem', margin: 0 }}>
                        <li>MediaPipe face detection</li>
                        <li>InsightFace embeddings</li>
                        <li>FAISS vector search</li>
                        <li>100% local processing</li>
                    </ul>
                </div>
            </div>

            {/* Info Section */}
            <div className="glass-card">
                <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>🚀 About HelloFace</h3>
                <p style={{ color: 'var(--color-text-secondary)', lineHeight: '1.8' }}>
                    HelloFace is a completely free and open-source face recognition system that runs entirely on your local machine.
                    No external APIs, no API keys, no paid services - just powerful computer vision technology accessible to everyone.
                </p>
                <div style={{ marginTop: '1.5rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                    <span className="badge">🆓 100% Free</span>
                    <span className="badge">🔒 Privacy-First</span>
                    <span className="badge">💻 CPU-Optimized</span>
                    <span className="badge">🌐 Open Source</span>
                </div>
            </div>
        </div>
    );
};

export default Home;

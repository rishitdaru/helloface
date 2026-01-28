import React, { useState } from 'react';
import WebcamCapture from '../components/WebcamCapture';
import { api } from '../api';

const Enroll = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [capturedImage, setCapturedImage] = useState(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState(null);
    const [messageType, setMessageType] = useState('success');

    const handleCapture = (imageSrc) => {
        setCapturedImage(imageSrc);
        setMessage(null);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!name || !email) {
            setMessage('Please fill in all fields');
            setMessageType('error');
            return;
        }

        if (!capturedImage) {
            setMessage('Please capture a photo');
            setMessageType('error');
            return;
        }

        setLoading(true);
        setMessage(null);

        try {
            const result = await api.enroll(name, email, capturedImage);
            setMessage(`✅ ${result.message}`);
            setMessageType('success');

            // Reset form
            setTimeout(() => {
                setName('');
                setEmail('');
                setCapturedImage(null);
                setMessage(null);
            }, 3000);
        } catch (error) {
            setMessage(`❌ ${error.message}`);
            setMessageType('error');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container" style={{ padding: '2rem 1rem', maxWidth: '800px' }}>
            <div className="text-center mb-2">
                <h1 style={{ background: 'var(--gradient-primary)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>
                    👤 Enroll New User
                </h1>
                <p className="text-muted">Register a new face in the system</p>
            </div>

            <div className="glass-card">
                <form onSubmit={handleSubmit}>
                    <div className="input-group">
                        <label className="input-label">Full Name</label>
                        <input
                            type="text"
                            className="input-field"
                            placeholder="Enter your full name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            disabled={loading}
                        />
                    </div>

                    <div className="input-group">
                        <label className="input-label">Email Address</label>
                        <input
                            type="email"
                            className="input-field"
                            placeholder="Enter your email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            disabled={loading}
                        />
                    </div>

                    <div className="input-group">
                        <label className="input-label">Capture Photo</label>
                        <WebcamCapture onCapture={handleCapture} showPreview={true} />
                    </div>

                    {message && (
                        <div className={`alert alert-${messageType}`}>
                            <span>{message}</span>
                        </div>
                    )}

                    <button
                        type="submit"
                        className="btn btn-primary"
                        disabled={loading || !capturedImage}
                        style={{ width: '100%', marginTop: '1rem' }}
                    >
                        {loading ? (
                            <>
                                <span className="spinner"></span>
                                <span>Enrolling...</span>
                            </>
                        ) : (
                            <>
                                <span>✨ Enroll User</span>
                            </>
                        )}
                    </button>
                </form>
            </div>

            <div className="glass-card mt-2">
                <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>📋 Instructions</h3>
                <ul style={{ color: 'var(--color-text-secondary)', paddingLeft: '1.5rem' }}>
                    <li>Ensure your face is well-lit and clearly visible</li>
                    <li>Look directly at the camera</li>
                    <li>Remove sunglasses or face coverings</li>
                    <li>Make sure only one face is in the frame</li>
                </ul>
            </div>
        </div>
    );
};

export default Enroll;

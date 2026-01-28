import React, { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import { api } from '../api';

const Recognize = () => {
    const webcamRef = useRef(null);
    const [recognizing, setRecognizing] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [lastImage, setLastImage] = useState(null);

    const videoConstraints = {
        width: 1280,
        height: 720,
        facingMode: 'user',
    };

    const recognizeFace = useCallback(async () => {
        if (!webcamRef.current) return;

        const imageSrc = webcamRef.current.getScreenshot();
        if (!imageSrc) return;

        setLastImage(imageSrc);
        setRecognizing(true);
        setError(null);

        try {
            const response = await api.recognize(imageSrc);
            setResult(response);
        } catch (err) {
            setError(err.message);
            setResult(null);
        } finally {
            setRecognizing(false);
        }
    }, [webcamRef]);

    const reset = () => {
        setResult(null);
        setError(null);
        setLastImage(null);
    };

    return (
        <div className="container" style={{ padding: '2rem 1rem', maxWidth: '1000px' }}>
            <div className="text-center mb-2">
                <h1 style={{ background: 'var(--gradient-accent)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>
                    🔍 Face Recognition
                </h1>
                <p className="text-muted">Identify enrolled users in real-time</p>
            </div>

            <div className="grid grid-2">
                {/* Webcam Section */}
                <div className="glass-card">
                    <h3 style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>📷 Camera</h3>

                    <div className="webcam-container">
                        {lastImage && result ? (
                            <img src={lastImage} alt="Last capture" className="webcam-video" />
                        ) : (
                            <Webcam
                                audio={false}
                                ref={webcamRef}
                                screenshotFormat="image/jpeg"
                                videoConstraints={videoConstraints}
                                className="webcam-video"
                            />
                        )}
                    </div>

                    <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem' }}>
                        {result ? (
                            <button onClick={reset} className="btn btn-secondary" style={{ flex: 1 }}>
                                🔄 Try Again
                            </button>
                        ) : (
                            <button
                                onClick={recognizeFace}
                                className="btn btn-primary"
                                disabled={recognizing}
                                style={{ flex: 1 }}
                            >
                                {recognizing ? (
                                    <>
                                        <span className="spinner"></span>
                                        <span>Recognizing...</span>
                                    </>
                                ) : (
                                    <>
                                        <span>🎯 Recognize Face</span>
                                    </>
                                )}
                            </button>
                        )}
                    </div>
                </div>

                {/* Results Section */}
                <div className="glass-card">
                    <h3 style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>📊 Results</h3>

                    {!result && !error && (
                        <div className="text-center" style={{ padding: '3rem 1rem', color: 'var(--color-text-muted)' }}>
                            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🤖</div>
                            <p>Click "Recognize Face" to identify a person</p>
                        </div>
                    )}

                    {error && (
                        <div className="alert alert-error">
                            <span>⚠️</span>
                            <span>{error}</span>
                        </div>
                    )}

                    {result && (
                        <div>
                            {result.recognized ? (
                                <div style={{ animation: 'slideIn 0.3s ease' }}>
                                    <div className="alert alert-success">
                                        <span>✅</span>
                                        <span>{result.message}</span>
                                    </div>

                                    <div style={{ marginTop: '1.5rem' }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
                                            <div style={{
                                                width: '60px',
                                                height: '60px',
                                                borderRadius: '50%',
                                                background: 'var(--gradient-primary)',
                                                display: 'flex',
                                                alignItems: 'center',
                                                justifyContent: 'center',
                                                fontSize: '2rem'
                                            }}>
                                                👤
                                            </div>
                                            <div>
                                                <h4 style={{ margin: 0, fontSize: '1.5rem' }}>{result.match.name}</h4>
                                                <p style={{ margin: 0, color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>
                                                    {result.match.email}
                                                </p>
                                            </div>
                                        </div>

                                        <div style={{ marginTop: '1.5rem' }}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                                <span style={{ fontWeight: 500 }}>Confidence Score</span>
                                                <span className="badge">{(result.match.confidence * 100).toFixed(1)}%</span>
                                            </div>
                                            <div className="confidence-bar">
                                                <div
                                                    className="confidence-fill"
                                                    style={{ width: `${result.match.confidence * 100}%` }}
                                                ></div>
                                            </div>
                                        </div>

                                        <div style={{ marginTop: '1.5rem', padding: '1rem', background: 'var(--color-bg-tertiary)', borderRadius: 'var(--radius-md)' }}>
                                            <div style={{ fontSize: '0.9rem', color: 'var(--color-text-secondary)' }}>
                                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                                    <span>User ID:</span>
                                                    <span style={{ fontWeight: 500, color: 'var(--color-text-primary)' }}>#{result.match.user_id}</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="alert alert-error">
                                    <span>❌</span>
                                    <span>{result.message}</span>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>

            <div className="glass-card mt-2">
                <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>💡 Tips</h3>
                <ul style={{ color: 'var(--color-text-secondary)', paddingLeft: '1.5rem' }}>
                    <li>Ensure good lighting for best results</li>
                    <li>Face the camera directly</li>
                    <li>Recognition threshold is set to 55% confidence</li>
                    <li>Higher confidence scores indicate better matches</li>
                </ul>
            </div>
        </div>
    );
};

export default Recognize;

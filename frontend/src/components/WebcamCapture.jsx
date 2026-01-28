import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';

const WebcamCapture = ({ onCapture, showPreview = true }) => {
    const webcamRef = useRef(null);
    const [imgSrc, setImgSrc] = useState(null);
    const [error, setError] = useState(null);

    const videoConstraints = {
        width: 1280,
        height: 720,
        facingMode: 'user',
    };

    const capture = useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        if (imageSrc) {
            setImgSrc(imageSrc);
            if (onCapture) {
                onCapture(imageSrc);
            }
        }
    }, [webcamRef, onCapture]);

    const retake = useCallback(() => {
        setImgSrc(null);
        if (onCapture) {
            onCapture(null);
        }
    }, [onCapture]);

    const handleUserMediaError = (error) => {
        console.error('Webcam error:', error);
        setError('Failed to access webcam. Please ensure you have granted camera permissions.');
    };

    return (
        <div className="webcam-wrapper">
            {error && (
                <div className="alert alert-error">
                    <span>⚠️</span>
                    <span>{error}</span>
                </div>
            )}

            <div className="webcam-container">
                {imgSrc && showPreview ? (
                    <img src={imgSrc} alt="Captured" className="webcam-video" />
                ) : (
                    <Webcam
                        audio={false}
                        ref={webcamRef}
                        screenshotFormat="image/jpeg"
                        videoConstraints={videoConstraints}
                        className="webcam-video"
                        onUserMediaError={handleUserMediaError}
                    />
                )}
            </div>

            <div className="webcam-controls" style={{ marginTop: '1rem', display: 'flex', gap: '1rem', justifyContent: 'center' }}>
                {imgSrc && showPreview ? (
                    <button onClick={retake} className="btn btn-secondary">
                        🔄 Retake Photo
                    </button>
                ) : (
                    <button onClick={capture} className="btn btn-primary">
                        📸 Capture Photo
                    </button>
                )}
            </div>
        </div>
    );
};

export default WebcamCapture;

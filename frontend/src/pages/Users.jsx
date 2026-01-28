import React, { useState, useEffect } from 'react';
import { api } from '../api';

const Users = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [deleting, setDeleting] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await api.getUsers();
            setUsers(data.users);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (userId, userName) => {
        if (!confirm(`Are you sure you want to delete ${userName}? This action cannot be undone.`)) {
            return;
        }

        setDeleting(userId);
        try {
            await api.deleteUser(userId);
            setUsers(users.filter(user => user.user_id !== userId));
        } catch (err) {
            alert(`Failed to delete user: ${err.message}`);
        } finally {
            setDeleting(null);
        }
    };

    const filteredUsers = users.filter(user =>
        user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.email.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <div className="container" style={{ padding: '2rem 1rem' }}>
            <div className="text-center mb-2">
                <h1 style={{ background: 'var(--gradient-secondary)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>
                    👥 Enrolled Users
                </h1>
                <p className="text-muted">Manage all registered users</p>
            </div>

            {/* Stats */}
            <div className="glass-card mb-2">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
                    <div>
                        <h3 style={{ fontSize: '2rem', margin: 0 }}>{users.length}</h3>
                        <p style={{ margin: 0, color: 'var(--color-text-muted)' }}>Total Users</p>
                    </div>
                    <button onClick={fetchUsers} className="btn btn-secondary" disabled={loading}>
                        {loading ? '🔄 Loading...' : '🔄 Refresh'}
                    </button>
                </div>
            </div>

            {/* Search */}
            <div className="glass-card mb-2">
                <input
                    type="text"
                    className="input-field"
                    placeholder="🔍 Search by name or email..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>

            {/* Error */}
            {error && (
                <div className="alert alert-error mb-2">
                    <span>⚠️</span>
                    <span>{error}</span>
                </div>
            )}

            {/* Users List */}
            {loading ? (
                <div className="glass-card text-center" style={{ padding: '3rem' }}>
                    <div className="spinner" style={{ width: '40px', height: '40px', margin: '0 auto' }}></div>
                    <p style={{ marginTop: '1rem', color: 'var(--color-text-muted)' }}>Loading users...</p>
                </div>
            ) : filteredUsers.length === 0 ? (
                <div className="glass-card text-center" style={{ padding: '3rem' }}>
                    <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>😔</div>
                    <h3>No users found</h3>
                    <p className="text-muted">
                        {searchTerm ? 'Try a different search term' : 'Start by enrolling your first user'}
                    </p>
                </div>
            ) : (
                <div className="grid" style={{ gap: '1rem' }}>
                    {filteredUsers.map((user) => (
                        <div key={user.user_id} className="glass-card">
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1rem' }}>
                                <div style={{ display: 'flex', gap: '1rem', flex: 1 }}>
                                    <div style={{
                                        width: '50px',
                                        height: '50px',
                                        borderRadius: '50%',
                                        background: 'var(--gradient-primary)',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        fontSize: '1.5rem',
                                        flexShrink: 0
                                    }}>
                                        👤
                                    </div>
                                    <div style={{ flex: 1, minWidth: 0 }}>
                                        <h4 style={{ margin: 0, marginBottom: '0.25rem', fontSize: '1.25rem' }}>
                                            {user.name}
                                        </h4>
                                        <p style={{ margin: 0, color: 'var(--color-text-muted)', fontSize: '0.9rem', wordBreak: 'break-word' }}>
                                            {user.email}
                                        </p>
                                        <p style={{ margin: 0, marginTop: '0.5rem', color: 'var(--color-text-muted)', fontSize: '0.85rem' }}>
                                            📅 Enrolled: {formatDate(user.enrolled_at)}
                                        </p>
                                        <p style={{ margin: 0, marginTop: '0.25rem', color: 'var(--color-text-muted)', fontSize: '0.85rem' }}>
                                            🆔 ID: #{user.user_id}
                                        </p>
                                    </div>
                                </div>
                                <button
                                    onClick={() => handleDelete(user.user_id, user.name)}
                                    className="btn btn-danger"
                                    disabled={deleting === user.user_id}
                                    style={{ padding: '0.5rem 1rem', fontSize: '0.9rem' }}
                                >
                                    {deleting === user.user_id ? '⏳' : '🗑️'}
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Users;

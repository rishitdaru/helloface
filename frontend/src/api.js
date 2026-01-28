const API_BASE_URL = 'http://localhost:8000';

export const api = {
    async enroll(name, email, imageBase64) {
        const response = await fetch(`${API_BASE_URL}/enroll`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name,
                email,
                image: imageBase64,
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Enrollment failed');
        }

        return response.json();
    },

    async recognize(imageBase64) {
        const response = await fetch(`${API_BASE_URL}/recognize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: imageBase64,
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Recognition failed');
        }

        return response.json();
    },

    async getUsers() {
        const response = await fetch(`${API_BASE_URL}/users`);

        if (!response.ok) {
            throw new Error('Failed to fetch users');
        }

        return response.json();
    },

    async deleteUser(userId) {
        const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to delete user');
        }

        return response.json();
    },

    async getStats() {
        const response = await fetch(`${API_BASE_URL}/stats`);

        if (!response.ok) {
            throw new Error('Failed to fetch stats');
        }

        return response.json();
    },

    async healthCheck() {
        const response = await fetch(`${API_BASE_URL}/health`);

        if (!response.ok) {
            throw new Error('Health check failed');
        }

        return response.json();
    },
};

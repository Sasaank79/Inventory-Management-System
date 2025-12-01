// Auth Helpers
const token = localStorage.getItem('token');

// Show/Hide Navbar based on auth
document.addEventListener('DOMContentLoaded', () => {
    if (token) {
        const nav = document.getElementById('navbar');
        if (nav) nav.style.display = 'block';
    } else if (window.location.pathname !== '/' && window.location.pathname !== '/login') {
        window.location.href = '/';
    }
});

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    window.location.href = '/';
}

async function apiCall(url, method = 'GET', body = null) {
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };

    const options = {
        method,
        headers
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);
    if (response.status === 401) {
        logout();
        return null;
    }
    return response;
}

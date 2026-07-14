// API Client and Core Utilities

const API_BASE_URL = 'http://127.0.0.1:5000/api';

class ApiClient {
  static async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    // Setup headers
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    // Attach JWT token if available
    const token = localStorage.getItem('access_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
      ...options,
      headers,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        if (response.status === 401 && !endpoint.includes('/auth/login')) {
          this.logout();
        }
        throw new Error(data.error || data.message || 'Something went wrong');
      }

      return data;
    } catch (error) {
      console.warn('API Error (Backend might be offline):', error);
      
      // MOCK FALLBACKS FOR HACKATHON DEMO (if backend is not running)
      if (endpoint === '/auth/register') {
        console.log("Mocking registration success for demo...");
        return { message: "Mock registration successful" };
      }
      
      if (endpoint === '/auth/login') {
        console.log("Mocking login success for demo...");
        const mockPayload = JSON.parse(options.body || '{}');
        const role = mockPayload.email.split('@')[0] || 'student'; // guess role from email
        return {
          access_token: "mock_token_123",
          refresh_token: "mock_refresh_123",
          user: { id: 1, email: mockPayload.email, first_name: "Demo", last_name: "User", role: role },
          profile: { id: 1 }
        };
      }

      throw new Error('Backend server is not running. Please start the Flask app or use demo mode.');
    }
  }

  static async login(email, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    if (data.profile) {
      localStorage.setItem('profile', JSON.stringify(data.profile));
    }
    
    return data;
  }

  static logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    localStorage.removeItem('profile');
    window.location.href = '/frontend/pages/login.html';
  }

  static getUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }
}

// Global UI Utilities
class UI {
  static showToast(message, type = 'success') {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }
}

window.API = ApiClient;
window.UI = UI;

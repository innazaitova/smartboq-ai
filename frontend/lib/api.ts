// API Client with authentication
import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Only redirect if we're not already on login/signup/public pages
      const publicPaths = ['/', '/login', '/signup', '/features', '/pricing', '/about', '/contact', '/demo', '/terms', '/privacy']
      const currentPath = typeof window !== 'undefined' ? window.location.pathname : ''
      
      // Clear auth data
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      
      // Only redirect if on protected page
      if (!publicPaths.includes(currentPath) && !currentPath.startsWith('/api/auth/')) {
        window.location.href = '/login?session_expired=true'
      }
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  register: async (email: string, password: string, fullName: string) => {
    const response = await apiClient.post('/api/auth/register', {
      email,
      password,
      full_name: fullName,
    })
    return response.data
  },

  login: async (email: string, password: string) => {
    const response = await apiClient.post('/api/auth/login', {
      email,
      password,
    })
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token)
    }
    return response.data
  },

  logout: () => {
    localStorage.removeItem('token')
  },

  getCurrentUser: async () => {
    const response = await apiClient.get('/api/auth/me')
    return response.data
  },
}

// Projects API
export const projectsAPI = {
  list: async () => {
    const response = await apiClient.get('/api/projects')
    return response.data
  },

  get: async (projectId: string) => {
    const response = await apiClient.get(`/api/projects/${projectId}`)
    return response.data
  },

  create: async (data: {
    project_name: string
    project_type: string
    location: string
    area_sqft?: number
  }) => {
    const response = await apiClient.post('/api/projects', data)
    return response.data
  },

  delete: async (projectId: string) => {
    const response = await apiClient.delete(`/api/projects/${projectId}`)
    return response.data
  },
}

// Alias for backward compatibility
export const projectAPI = {
  createProject: projectsAPI.create,
  getProject: projectsAPI.get,
  listProjects: projectsAPI.list,
  deleteProject: projectsAPI.delete,
}

// Drawings API
export const drawingsAPI = {
  upload: async (projectId: string, file: File) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await apiClient.post(
      `/projects/${projectId}/drawings/upload`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    )
    return response.data
  },

  list: async (projectId: string) => {
    const response = await apiClient.get(`/projects/${projectId}/drawings`)
    return response.data
  },

  get: async (drawingId: string) => {
    const response = await apiClient.get(`/drawings/${drawingId}`)
    return response.data
  },

  delete: async (drawingId: string) => {
    const response = await apiClient.delete(`/drawings/${drawingId}`)
    return response.data
  },
}

// Processing API
export const processingAPI = {
  analyzeDrawing: async (drawingId: string) => {
    const response = await apiClient.post(`/process/analyze/${drawingId}`)
    return response.data
  },

  calculateQuantities: async (drawingId: string) => {
    const response = await apiClient.post(`/process/quantities/${drawingId}`)
    return response.data
  },

  estimateCosts: async (projectId: string) => {
    const response = await apiClient.post(`/process/costs/${projectId}`)
    return response.data
  },

  generateBOQ: async (projectId: string, format: 'excel' | 'pdf' = 'excel') => {
    const response = await apiClient.post(`/process/boq/${projectId}`, {
      format,
    })
    return response.data
  },

  getStatus: async (taskId: string) => {
    const response = await apiClient.get(`/process/status/${taskId}`)
    return response.data
  },
}

// BOQ API
export const boqAPI = {
  download: async (projectId: string) => {
    const response = await apiClient.get(`/boq/${projectId}/download`, {
      responseType: 'blob',
    })
    return response.data
  },

  preview: async (projectId: string) => {
    const response = await apiClient.get(`/boq/${projectId}/preview`)
    return response.data
  },
}

// Subscription API
export const subscriptionAPI = {
  getCurrentPlan: async () => {
    const response = await apiClient.get('/subscription/current')
    return response.data
  },

  createCheckoutSession: async (planId: string) => {
    const response = await apiClient.post('/subscription/checkout', {
      plan_id: planId,
    })
    return response.data
  },

  cancelSubscription: async () => {
    const response = await apiClient.post('/subscription/cancel')
    return response.data
  },

  getUsage: async () => {
    const response = await apiClient.get('/subscription/usage')
    return response.data
  },
}

// Analytics API
export const analyticsAPI = {
  getDashboardStats: async () => {
    const response = await apiClient.get('/analytics/dashboard')
    return response.data
  },

  getProjectStats: async (projectId: string) => {
    const response = await apiClient.get(`/analytics/project/${projectId}`)
    return response.data
  },
}

export default apiClient

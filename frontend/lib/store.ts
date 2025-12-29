// State Management with Zustand
import { create } from 'zustand'
import { authAPI } from './api'

interface User {
  id: string
  email: string
  full_name: string
  subscription_tier: string
  subscription_status: string
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, fullName: string) => Promise<void>
  logout: () => void
  checkAuth: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  login: async (email: string, password: string) => {
    try {
      set({ isLoading: true, error: null })
      await authAPI.login(email, password)
      const user = await authAPI.getCurrentUser()
      // Persist user data for faster auth restoration
      localStorage.setItem('user', JSON.stringify(user))
      set({ user, isAuthenticated: true, isLoading: false })
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Login failed',
        isLoading: false 
      })
      throw error
    }
  },

  register: async (email: string, password: string, fullName: string) => {
    try {
      set({ isLoading: true, error: null })
      await authAPI.register(email, password, fullName)
      await authAPI.login(email, password)
      const user = await authAPI.getCurrentUser()
      // Persist user data for faster auth restoration
      localStorage.setItem('user', JSON.stringify(user))
      set({ user, isAuthenticated: true, isLoading: false })
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Registration failed',
        isLoading: false 
      })
      throw error
    }
  },

  logout: () => {
    authAPI.logout()
    localStorage.removeItem('user')
    set({ user: null, isAuthenticated: false })
  },

  checkAuth: async () => {
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        localStorage.removeItem('user')
        set({ isLoading: false, isAuthenticated: false, user: null })
        return
      }

      // Restore from localStorage immediately for instant UI
      const cachedUser = localStorage.getItem('user')
      if (cachedUser) {
        try {
          const user = JSON.parse(cachedUser)
          set({ user, isAuthenticated: true, isLoading: false })
        } catch (e) {
          // Invalid cached data, clear it
          localStorage.removeItem('user')
        }
      }

      // Validate token with API in background
      try {
        const user = await authAPI.getCurrentUser()
        localStorage.setItem('user', JSON.stringify(user))
        set({ user, isAuthenticated: true, isLoading: false })
      } catch (error: any) {
        // Only logout on 401 (invalid token), not on network errors
        if (error.response?.status === 401) {
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          set({ isLoading: false, isAuthenticated: false, user: null })
        }
        // For other errors (network, etc), keep user logged in with cached data
      }
    } catch (error) {
      // Only clear on critical errors
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      set({ isLoading: false, isAuthenticated: false, user: null })
    }
  },
}))

// Project State
interface Project {
  id: string
  name: string
  description: string
  project_type: string
  location: string
  region: string
  status: string
  created_at: string
}

interface ProjectState {
  projects: Project[]
  currentProject: Project | null
  isLoading: boolean
  fetchProjects: () => Promise<void>
  setCurrentProject: (project: Project) => void
}

export const useProjectStore = create<ProjectState>((set) => ({
  projects: [],
  currentProject: null,
  isLoading: false,

  fetchProjects: async () => {
    try {
      set({ isLoading: true })
      const { projectsAPI } = await import('./api')
      const projects = await projectsAPI.list()
      set({ projects, isLoading: false })
    } catch (error) {
      set({ isLoading: false })
    }
  },

  setCurrentProject: (project: Project) => {
    set({ currentProject: project })
  },
}))

// Processing State
interface ProcessingState {
  isProcessing: boolean
  progress: number
  currentStep: string
  taskId: string | null
  setProcessing: (isProcessing: boolean) => void
  setProgress: (progress: number, step: string) => void
  setTaskId: (taskId: string) => void
}

export const useProcessingStore = create<ProcessingState>((set) => ({
  isProcessing: false,
  progress: 0,
  currentStep: '',
  taskId: null,

  setProcessing: (isProcessing: boolean) => {
    set({ isProcessing })
  },

  setProgress: (progress: number, step: string) => {
    set({ progress, currentStep: step })
  },

  setTaskId: (taskId: string) => {
    set({ taskId })
  },
}))

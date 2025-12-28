'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore, useProjectStore } from '../../lib/store'
import Link from 'next/link'
import { 
  Plus, 
  FileText, 
  Clock, 
  DollarSign, 
  TrendingUp,
  Upload,
  CheckCircle,
  AlertCircle 
} from 'lucide-react'

export default function DashboardPage() {
  const router = useRouter()
  const { user, isAuthenticated, isLoading: authLoading, checkAuth } = useAuthStore()
  const { projects, fetchProjects, isLoading: projectsLoading } = useProjectStore()
  const [stats, setStats] = useState({
    totalProjects: 0,
    completedProjects: 0,
    totalSavings: 0,
    avgProcessingTime: 0,
  })

  useEffect(() => {
    checkAuth()
  }, [])

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login')
    } else if (isAuthenticated) {
      fetchProjects()
    }
  }, [authLoading, isAuthenticated])

  useEffect(() => {
    if (projects.length > 0) {
      const completed = projects.filter(p => p.status === 'completed').length
      setStats({
        totalProjects: projects.length,
        completedProjects: completed,
        totalSavings: completed * 2500, // Avg $2,500 saved per project
        avgProcessingTime: 28, // minutes
      })
    }
  }, [projects])

  if (authLoading || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <Link href="/" className="text-2xl font-bold text-blue-600">
              QuantiBot AI
            </Link>
            <nav className="flex items-center space-x-6">
              <Link href="/dashboard" className="text-gray-700 hover:text-blue-600">
                Dashboard
              </Link>
              <Link href="/projects" className="text-gray-700 hover:text-blue-600">
                Projects
              </Link>
              <div className="relative">
                <button className="flex items-center space-x-2 text-gray-700">
                  <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                    {user?.full_name?.charAt(0) || 'U'}
                  </div>
                  <span>{user?.full_name}</span>
                </button>
              </div>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.full_name?.split(' ')[0]}!
          </h1>
          <p className="text-gray-600 mt-2">
            Here's what's happening with your projects today
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <StatCard
            icon={<FileText className="w-8 h-8 text-blue-600" />}
            title="Total Projects"
            value={stats.totalProjects}
            subtext="All time"
          />
          <StatCard
            icon={<CheckCircle className="w-8 h-8 text-green-600" />}
            title="Completed"
            value={stats.completedProjects}
            subtext={`${stats.completedProjects > 0 ? ((stats.completedProjects / stats.totalProjects) * 100).toFixed(0) : 0}% completion rate`}
          />
          <StatCard
            icon={<DollarSign className="w-8 h-8 text-emerald-600" />}
            title="Total Savings"
            value={`$${stats.totalSavings.toLocaleString()}`}
            subtext="vs manual QS"
          />
          <StatCard
            icon={<Clock className="w-8 h-8 text-purple-600" />}
            title="Avg Processing"
            value={`${stats.avgProcessingTime} min`}
            subtext="40x faster"
          />
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
          <div className="grid md:grid-cols-3 gap-4">
            <Link
              href="/projects/new"
              className="flex items-center space-x-3 p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-600 hover:bg-blue-50 transition-colors"
            >
              <Plus className="w-6 h-6 text-blue-600" />
              <div>
                <div className="font-semibold">New Project</div>
                <div className="text-sm text-gray-600">Start fresh analysis</div>
              </div>
            </Link>
            <Link
              href="/upload"
              className="flex items-center space-x-3 p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-600 hover:bg-blue-50 transition-colors"
            >
              <Upload className="w-6 h-6 text-blue-600" />
              <div>
                <div className="font-semibold">Upload Drawings</div>
                <div className="text-sm text-gray-600">Add to existing project</div>
              </div>
            </Link>
          </div>
        </div>

        {/* Recent Projects */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold">Recent Projects</h2>
              <Link href="/projects" className="text-blue-600 hover:underline">
                View all
              </Link>
            </div>
          </div>
          <div className="p-6">
            {projectsLoading ? (
              <div className="text-center py-8">
                <div className="spinner mx-auto"></div>
                <p className="text-gray-600 mt-4">Loading projects...</p>
              </div>
            ) : projects.length === 0 ? (
              <div className="text-center py-12">
                <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  No projects yet
                </h3>
                <p className="text-gray-600 mb-4">
                  Create your first project to get started
                </p>
                <Link
                  href="/projects/new"
                  className="inline-flex items-center bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
                >
                  <Plus className="w-5 h-5 mr-2" />
                  Create Project
                </Link>
              </div>
            ) : (
              <div className="space-y-4">
                {projects.slice(0, 5).map((project) => (
                  <ProjectCard key={project.id} project={project} />
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

function StatCard({ icon, title, value, subtext }: any) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
          <p className="text-sm text-gray-500 mt-1">{subtext}</p>
        </div>
        <div>{icon}</div>
      </div>
    </div>
  )
}

function ProjectCard({ project }: any) {
  const statusColors: any = {
    draft: 'bg-gray-100 text-gray-800',
    processing: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    error: 'bg-red-100 text-red-800',
  }

  return (
    <Link
      href={`/projects/${project.id}`}
      className="block border rounded-lg p-4 hover:shadow-md transition-shadow"
    >
      <div className="flex justify-between items-start">
        <div className="flex-1">
          <h3 className="font-semibold text-gray-900 mb-1">{project.name}</h3>
          <p className="text-sm text-gray-600 mb-2">{project.description || 'No description'}</p>
          <div className="flex items-center space-x-4 text-sm text-gray-500">
            <span>{project.project_type}</span>
            <span>•</span>
            <span>{project.location}</span>
            <span>•</span>
            <span>{new Date(project.created_at).toLocaleDateString()}</span>
          </div>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${statusColors[project.status]}`}>
          {project.status}
        </span>
      </div>
    </Link>
  )
}

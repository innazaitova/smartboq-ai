'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { useAuthStore } from '../../../lib/store'
import Link from 'next/link'
import { ArrowLeft, Upload, FileText, Download, Clock, DollarSign, AlertCircle } from 'lucide-react'
import { projectAPI } from '../../../lib/api'
import toast from 'react-hot-toast'

export default function ProjectDetailPage() {
  const router = useRouter()
  const params = useParams()
  const projectId = params.id as string
  const { user, isAuthenticated, checkAuth } = useAuthStore()
  const [project, setProject] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)

  useEffect(() => {
    checkAuth()
  }, [])

  useEffect(() => {
    if (isAuthenticated && projectId) {
      loadProject()
    } else if (!isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, projectId])

  const loadProject = async () => {
    try {
      const data = await projectAPI.getProject(projectId)
      setProject(data)
    } catch (error: any) {
      toast.error('Failed to load project')
      router.push('/projects')
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (!files || files.length === 0) return

    setUploading(true)
    try {
      const formData = new FormData()
      for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i])
      }

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const token = localStorage.getItem('token')
      const response = await fetch(`${apiUrl}/api/projects/${projectId}/drawings`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Upload failed')
      }

      const result = await response.json()
      toast.success(result.message)
      
      // Reload project to show uploaded drawings
      setTimeout(() => {
        loadProject()
      }, 1000)
    } catch (error: any) {
      toast.error(error.message || 'Failed to upload files')
    } finally {
      setUploading(false)
    }
  }

  if (loading || !project) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner"></div>
      </div>
    )
  }

  const statusColors: any = {
    created: 'bg-gray-100 text-gray-800',
    processing: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    error: 'bg-red-100 text-red-800',
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
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                {user?.full_name?.charAt(0) || 'U'}
              </div>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <Link href="/projects" className="inline-flex items-center text-blue-600 hover:underline mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Projects
          </Link>
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{project.project.project_name}</h1>
              <p className="text-gray-600 mt-2">{project.project.project_type} • {project.project.location}</p>
            </div>
            <span className={`px-4 py-2 rounded-full text-sm font-semibold ${statusColors[project.project.status]}`}>
              {project.project.status}
            </span>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-600">Area</span>
              <FileText className="w-5 h-5 text-blue-600" />
            </div>
            <div className="text-2xl font-bold">{project.project.area_sqft?.toLocaleString() || 'N/A'} sq ft</div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-600">Drawings</span>
              <Upload className="w-5 h-5 text-blue-600" />
            </div>
            <div className="text-2xl font-bold">{project.drawings?.length || 0}</div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-600">Created</span>
              <Clock className="w-5 h-5 text-blue-600" />
            </div>
            <div className="text-2xl font-bold">
              {new Date(project.project.created_at).toLocaleDateString()}
            </div>
          </div>
        </div>

        {/* Upload Section */}
        {project.project.status === 'created' && (
          <div className="bg-white rounded-lg shadow p-8 mb-8">
            <h2 className="text-xl font-semibold mb-4">Upload Construction Drawings</h2>
            <p className="text-gray-600 mb-6">
              Upload your construction drawings (PDF, DWG, DXF, or images) to start AI analysis
            </p>
            
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-600 transition-colors">
              <Upload className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Drop files here or click to browse</h3>
              <p className="text-gray-600 mb-4">Supports PDF, DWG, DXF, PNG, JPG (Max 50MB per file)</p>
              <label className="inline-block">
                <input
                  type="file"
                  multiple
                  accept=".pdf,.dwg,.dxf,.png,.jpg,.jpeg"
                  onChange={handleFileUpload}
                  className="hidden"
                  disabled={uploading}
                />
                <span className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 cursor-pointer inline-block">
                  {uploading ? 'Uploading...' : 'Select Files'}
                </span>
              </label>
            </div>
          </div>
        )}

        {/* Drawings List */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Uploaded Drawings</h2>
          {project.drawings?.length === 0 ? (
            <div className="text-center py-8 text-gray-600">
              <FileText className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p>No drawings uploaded yet</p>
            </div>
          ) : (
            <div className="space-y-3">
              {project.drawings?.map((drawing: any) => (
                <div key={drawing.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <FileText className="w-5 h-5 text-blue-600" />
                    <div>
                      <div className="font-semibold">{drawing.file_name}</div>
                      <div className="text-sm text-gray-600">{drawing.file_type}</div>
                    </div>
                  </div>
                  <button className="text-blue-600 hover:underline">
                    <Download className="w-5 h-5" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* BOQ Section */}
        {project.project.status === 'completed' && (
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Bill of Quantities</h2>
              <button className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 flex items-center gap-2">
                <Download className="w-5 h-5" />
                Download BOQ
              </button>
            </div>
            <div className="text-center py-12 text-gray-600">
              <p>BOQ preview and download functionality coming soon</p>
            </div>
          </div>
        )}

        {/* Processing Status */}
        {project.project.status === 'processing' && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <div className="flex items-start gap-4">
              <div className="spinner"></div>
              <div className="flex-1">
                <h3 className="font-semibold text-blue-900 mb-2">Processing Drawings...</h3>
                <p className="text-blue-800">
                  Our AI is analyzing your drawings. This usually takes 15-30 minutes.
                  You'll receive an email when it's ready.
                </p>
              </div>
              <button
                onClick={async () => {
                  try {
                    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
                    const token = localStorage.getItem('token')
                    const response = await fetch(`${apiUrl}/api/projects/${projectId}/process`, {
                      method: 'POST',
                      headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                      }
                    })
                    if (response.ok) {
                      toast.success('Processing restarted')
                      setTimeout(() => loadProject(), 2000)
                    }
                  } catch (error) {
                    toast.error('Failed to restart processing')
                  }
                }}
                className="text-sm text-blue-600 hover:underline"
              >
                Restart
              </button>
            </div>
          </div>
        )}

        {/* Error Status */}
        {project.project.status === 'error' && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 flex items-start gap-4">
            <AlertCircle className="w-6 h-6 text-red-600 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-red-900 mb-2">Processing Error</h3>
              <p className="text-red-800">
                There was an error processing your drawings. Please contact support or try uploading again.
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

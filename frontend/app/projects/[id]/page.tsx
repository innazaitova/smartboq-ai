'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { useAuthStore } from '../../../lib/store'
import Link from 'next/link'
import { ArrowLeft, Upload, FileText, Download, Clock, DollarSign, AlertCircle, Edit2, Trash2, RefreshCw } from 'lucide-react'
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
  const [showEditModal, setShowEditModal] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [editForm, setEditForm] = useState({
    project_name: '',
    project_type: '',
    location: '',
    area_sqft: 0
  })

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
      setEditForm({
        project_name: data.project.project_name,
        project_type: data.project.project_type,
        location: data.project.location,
        area_sqft: data.project.area_sqft
      })
    } catch (error: any) {
      toast.error('Failed to load project')
      router.push('/projects')
    } finally {
      setLoading(false)
    }
  }

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const token = localStorage.getItem('token')
      const response = await fetch(`${apiUrl}/api/projects/${projectId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(editForm)
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Update failed')
      }

      toast.success('Project updated successfully!')
      setShowEditModal(false)
      loadProject()
    } catch (error: any) {
      toast.error(error.message || 'Failed to update project')
    }
  }

  const handleDelete = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const token = localStorage.getItem('token')
      const response = await fetch(`${apiUrl}/api/projects/${projectId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Delete failed')
      }

      toast.success('Project deleted successfully!')
      router.push('/projects')
    } catch (error: any) {
      toast.error(error.message || 'Failed to delete project')
    }
  }

  const handleDeleteDrawing = async (drawingId: number) => {
    if (!confirm('Are you sure you want to delete this drawing?')) return
    
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const token = localStorage.getItem('token')
      const response = await fetch(`${apiUrl}/api/projects/${projectId}/drawings/${drawingId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Delete failed')
      }

      toast.success('Drawing deleted successfully!')
      loadProject()
    } catch (error: any) {
      toast.error(error.message || 'Failed to delete drawing')
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
            <div className="flex items-center gap-3">
              <span className={`px-4 py-2 rounded-full text-sm font-semibold ${statusColors[project.project.status]}`}>
                {project.project.status}
              </span>
              <button
                onClick={() => setShowEditModal(true)}
                className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition"
                title="Edit Project"
              >
                <Edit2 className="w-4 h-4" />
                Edit
              </button>
              <button
                onClick={() => setShowDeleteModal(true)}
                className="flex items-center gap-2 px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition"
                title="Delete Project"
              >
                <Trash2 className="w-4 h-4" />
                Delete
              </button>
            </div>
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

        {/* Upload Section - Always show for re-uploading */}
        <div className="bg-white rounded-lg shadow p-8 mb-8">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h2 className="text-xl font-semibold">Upload Construction Drawings</h2>
              <p className="text-gray-600 mt-1">
                {project.drawings?.length > 0 ? 'Add more drawings or re-upload' : 'Upload your construction drawings to start AI analysis'}
              </p>
            </div>
            {project.drawings?.length > 0 && (
              <RefreshCw className="w-6 h-6 text-blue-600" />
            )}
          </div>
            
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-600 transition-colors">
            <Upload className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">Drop files here or click to browse</h3>
            <p className="text-gray-600 mb-4">Supports PDF, PNG, JPG (Max 25MB per file, 10 files max)</p>
            <label className="inline-block">
              <input
                type="file"
                multiple
                accept=".pdf,.png,.jpg,.jpeg"
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

        {/* Drawings List */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Uploaded Drawings ({project.drawings?.length || 0})</h2>
          {project.drawings?.length === 0 ? (
            <div className="text-center py-8 text-gray-600">
              <FileText className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p>No drawings uploaded yet</p>
            </div>
          ) : (
            <div className="space-y-3">
              {project.drawings?.map((drawing: any) => (
                <div key={drawing.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition">
                  <div className="flex items-center gap-3">
                    <FileText className="w-5 h-5 text-blue-600" />
                    <div>
                      <div className="font-semibold">{drawing.file_name}</div>
                      <div className="text-sm text-gray-600">
                        {drawing.drawing_type} • Status: {drawing.status}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button 
                      onClick={() => handleDeleteDrawing(drawing.id)}
                      className="text-red-600 hover:bg-red-50 p-2 rounded transition"
                      title="Delete drawing"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* BOQ Section */}
        {project.project.status === 'completed' && project.quantities_count > 0 && (
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h2 className="text-xl font-semibold">Bill of Quantities</h2>
                <p className="text-gray-600 mt-1">{project.quantities_count} elements detected</p>
              </div>
              <button 
                onClick={async () => {
                  try {
                    toast.loading('Generating BOQ...')
                    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
                    const token = localStorage.getItem('token')
                    const response = await fetch(`${apiUrl}/api/projects/${projectId}/boq/download?format=excel`, {
                      method: 'GET',
                      headers: {
                        'Authorization': `Bearer ${token}`
                      }
                    })

                    if (!response.ok) {
                      const error = await response.json()
                      throw new Error(error.detail || 'Failed to generate BOQ')
                    }

                    // Download file
                    const blob = await response.blob()
                    const url = window.URL.createObjectURL(blob)
                    const a = document.createElement('a')
                    a.href = url
                    a.download = `${project.project.project_name}_BOQ.xlsx`
                    document.body.appendChild(a)
                    a.click()
                    window.URL.revokeObjectURL(url)
                    document.body.removeChild(a)
                    
                    toast.dismiss()
                    toast.success('BOQ downloaded successfully!')
                  } catch (error: any) {
                    toast.dismiss()
                    toast.error(error.message || 'Failed to download BOQ')
                  }
                }}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 flex items-center gap-2 transition"
              >
                <Download className="w-5 h-5" />
                Download Excel BOQ
              </button>
            </div>
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-8 text-center">
              <div className="max-w-2xl mx-auto">
                <FileText className="w-16 h-16 text-blue-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Your BOQ is Ready!</h3>
                <p className="text-gray-700 mb-4">
                  Click the button above to download a professional Excel spreadsheet with all detected quantities, 
                  including columns, beams, walls, doors, windows, and other construction elements.
                </p>
                <div className="grid grid-cols-3 gap-4 mt-6 text-sm">
                  <div className="bg-white p-4 rounded-lg">
                    <div className="font-semibold text-blue-600 text-2xl mb-1">{project.quantities_count}</div>
                    <div className="text-gray-600">Elements</div>
                  </div>
                  <div className="bg-white p-4 rounded-lg">
                    <div className="font-semibold text-blue-600 text-2xl mb-1">{project.drawings?.length || 0}</div>
                    <div className="text-gray-600">Drawings</div>
                  </div>
                  <div className="bg-white p-4 rounded-lg">
                    <div className="font-semibold text-blue-600 text-2xl mb-1">Excel</div>
                    <div className="text-gray-600">Format</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* No Elements Detected */}
        {project.project.status === 'completed' && project.quantities_count === 0 && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 flex items-start gap-4">
            <AlertCircle className="w-6 h-6 text-yellow-600 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-yellow-900 mb-2">No Elements Detected</h3>
              <p className="text-yellow-800 mb-3">
                The AI couldn't detect any construction elements in your drawings. This might be because:
              </p>
              <ul className="list-disc list-inside text-yellow-800 space-y-1 mb-4">
                <li>The drawings are not construction/architectural plans</li>
                <li>The drawings lack text specifications or clear dimensions</li>
                <li>The image quality is too low for analysis</li>
              </ul>
              <p className="text-yellow-800">
                Please try uploading clearer drawings with visible specifications, or upload a PDF with construction text.
              </p>
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

      {/* Edit Modal */}
      {showEditModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full p-6">
            <h2 className="text-2xl font-bold mb-6">Edit Project</h2>
            <form onSubmit={handleUpdate} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Project Name *
                </label>
                <input
                  type="text"
                  value={editForm.project_name}
                  onChange={(e) => setEditForm({...editForm, project_name: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Project Type *
                </label>
                <select
                  value={editForm.project_type}
                  onChange={(e) => setEditForm({...editForm, project_type: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                  required
                >
                  <option value="">Select Type</option>
                  <option value="Residential">Residential</option>
                  <option value="Commercial">Commercial</option>
                  <option value="Industrial">Industrial</option>
                  <option value="Infrastructure">Infrastructure</option>
                  <option value="Renovation">Renovation</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Location *
                </label>
                <input
                  type="text"
                  value={editForm.location}
                  onChange={(e) => setEditForm({...editForm, location: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Area (sq ft)
                </label>
                <input
                  type="number"
                  value={editForm.area_sqft}
                  onChange={(e) => setEditForm({...editForm, area_sqft: parseFloat(e.target.value)})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                  min="0"
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
                >
                  Save Changes
                </button>
                <button
                  type="button"
                  onClick={() => setShowEditModal(false)}
                  className="flex-1 bg-gray-200 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-300 transition"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <div className="flex items-start gap-4 mb-6">
              <div className="bg-red-100 p-3 rounded-full">
                <AlertCircle className="w-6 h-6 text-red-600" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-2">Delete Project?</h2>
                <p className="text-gray-600">
                  This will permanently delete "{project.project.project_name}" and all its drawings.
                  This action cannot be undone.
                </p>
              </div>
            </div>

            <div className="flex gap-3">
              <button
                onClick={handleDelete}
                className="flex-1 bg-red-600 text-white py-3 rounded-lg font-semibold hover:bg-red-700 transition"
              >
                Yes, Delete
              </button>
              <button
                onClick={() => setShowDeleteModal(false)}
                className="flex-1 bg-gray-200 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-300 transition"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

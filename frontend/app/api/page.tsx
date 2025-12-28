import Link from 'next/link'

export default function APIPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-blue-600">
            QuantiBot AI
          </Link>
          <div className="space-x-6">
            <Link href="/features" className="text-gray-600 hover:text-gray-900">
              Features
            </Link>
            <Link href="/pricing" className="text-gray-600 hover:text-gray-900">
              Pricing
            </Link>
            <Link href="/login" className="text-gray-600 hover:text-gray-900">
              Login
            </Link>
            <Link 
              href="/signup" 
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
            >
              Start Free Trial
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          QuantiBot API
        </h1>
        <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
          Integrate AI-powered quantity surveying directly into your construction software, ERP system, or workflow.
        </p>
      </section>

      {/* Features */}
      <section className="container mx-auto px-4 py-20">
        <h2 className="text-4xl font-bold text-center mb-16">API Features</h2>
        
        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <APIFeature
            title="RESTful API"
            description="Simple REST endpoints for uploading drawings, processing projects, and retrieving BOQs."
          />
          <APIFeature
            title="Webhook Support"
            description="Real-time notifications when processing is complete or errors occur."
          />
          <APIFeature
            title="Batch Processing"
            description="Upload and process multiple projects simultaneously for faster turnaround."
          />
          <APIFeature
            title="Custom Export"
            description="Generate BOQs in your preferred format - JSON, XML, Excel, or PDF."
          />
        </div>
      </section>

      {/* Example */}
      <section className="bg-white py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16">Quick Start Example</h2>
          
          <div className="max-w-3xl mx-auto">
            <div className="bg-gray-900 text-white p-6 rounded-lg overflow-x-auto">
              <pre className="text-sm">
{`// Upload a drawing for processing
const response = await fetch('https://api.quantibot.ai/v1/projects', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    project_name: 'Residential Building',
    drawing_url: 'https://your-storage.com/drawing.pdf'
  })
});

const project = await response.json();
// { project_id: '12345', status: 'processing' }

// Check processing status
const status = await fetch(
  \`https://api.quantibot.ai/v1/projects/\${project.project_id}\`,
  {
    headers: { 'Authorization': 'Bearer YOUR_API_KEY' }
  }
);

// Download BOQ when ready
const boq = await fetch(
  \`https://api.quantibot.ai/v1/projects/\${project.project_id}/boq\`,
  {
    headers: { 'Authorization': 'Bearer YOUR_API_KEY' }
  }
);`}
              </pre>
            </div>
          </div>
        </div>
      </section>

      {/* Endpoints */}
      <section className="container mx-auto px-4 py-20">
        <h2 className="text-4xl font-bold text-center mb-16">API Endpoints</h2>
        
        <div className="max-w-4xl mx-auto space-y-6">
          <Endpoint
            method="POST"
            path="/v1/projects"
            description="Create a new project and upload drawing"
          />
          <Endpoint
            method="GET"
            path="/v1/projects/{id}"
            description="Get project status and details"
          />
          <Endpoint
            method="GET"
            path="/v1/projects/{id}/boq"
            description="Download generated BOQ"
          />
          <Endpoint
            method="GET"
            path="/v1/projects"
            description="List all your projects"
          />
          <Endpoint
            method="DELETE"
            path="/v1/projects/{id}"
            description="Delete a project"
          />
        </div>
      </section>

      {/* Pricing */}
      <section className="bg-blue-600 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">API Pricing</h2>
          <div className="max-w-2xl mx-auto">
            <div className="bg-white text-gray-900 rounded-xl p-8 mb-8">
              <div className="text-3xl font-bold mb-2">$0.50 per API call</div>
              <p className="text-gray-600">Pay as you go, no monthly minimum</p>
            </div>
            <p className="text-blue-100 mb-8">
              Or get API access included with Professional ($997/month) and Enterprise plans
            </p>
            <Link 
              href="/contact"
              className="bg-white text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 inline-block"
            >
              Get API Access
            </Link>
          </div>
        </div>
      </section>

      {/* Documentation */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h2 className="text-4xl font-bold mb-6">Need Full Documentation?</h2>
        <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
          Complete API documentation with authentication, rate limits, error handling, and code samples in multiple languages.
        </p>
        <Link 
          href="/signup"
          className="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 inline-block"
        >
          Sign Up to Access Docs
        </Link>
      </section>
    </div>
  )
}

function APIFeature({ title, description }: any) {
  return (
    <div className="p-6 border rounded-lg">
      <h3 className="text-xl font-bold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}

function Endpoint({ method, path, description }: any) {
  const methodColors: any = {
    GET: 'bg-green-100 text-green-700',
    POST: 'bg-blue-100 text-blue-700',
    PUT: 'bg-yellow-100 text-yellow-700',
    DELETE: 'bg-red-100 text-red-700'
  }
  
  return (
    <div className="border rounded-lg p-6 flex items-start gap-4">
      <span className={`px-3 py-1 rounded font-mono text-sm font-semibold ${methodColors[method]}`}>
        {method}
      </span>
      <div className="flex-1">
        <code className="text-lg font-mono text-gray-900">{path}</code>
        <p className="text-gray-600 mt-2">{description}</p>
      </div>
    </div>
  )
}

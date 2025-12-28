import Link from 'next/link'

export default function DemoPage() {
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
          See QuantiBot AI in Action
        </h1>
        <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
          Watch how we transform a complex construction drawing into a complete BOQ in just 30 minutes.
        </p>
      </section>

      {/* Video Section */}
      <section className="container mx-auto px-4 pb-20">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gray-900 rounded-xl overflow-hidden shadow-2xl aspect-video flex items-center justify-center">
            <div className="text-center text-white">
              <div className="text-6xl mb-4">▶️</div>
              <p className="text-xl mb-2">Demo Video Coming Soon</p>
              <p className="text-gray-400">Upload a sample drawing and see instant results</p>
            </div>
          </div>
          
          <div className="mt-12 text-center">
            <h2 className="text-3xl font-bold mb-6">Want to Try It Yourself?</h2>
            <Link 
              href="/signup"
              className="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 inline-block"
            >
              Start Free Trial - Process Your First Drawing
            </Link>
          </div>
        </div>
      </section>

      {/* Demo Steps */}
      <section className="bg-white py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16">Demo Walkthrough</h2>
          
          <div className="max-w-4xl mx-auto space-y-12">
            <DemoStep
              number="1"
              title="Upload Drawing"
              description="Drag and drop your construction PDF or DWG file. In this demo, we'll use a 2-story residential building plan."
              time="30 seconds"
            />
            
            <DemoStep
              number="2"
              title="AI Analysis"
              description="Watch as GPT-4o identifies walls, beams, columns, slabs, doors, windows, and all structural elements with 95%+ accuracy."
              time="5-10 minutes"
            />
            
            <DemoStep
              number="3"
              title="Quantity Calculation"
              description="Automatic calculation of concrete volumes, steel quantities, brick work areas, and more - all compliant with IS codes."
              time="3-5 minutes"
            />
            
            <DemoStep
              number="4"
              title="BOQ Generation"
              description="Professional Bill of Quantities formatted to IS 1200 standards, complete with item codes, descriptions, units, and quantities."
              time="2 minutes"
            />
            
            <DemoStep
              number="5"
              title="Cost Estimation"
              description="Real-time cost estimation using current market rates for materials and labor in your project location."
              time="1 minute"
            />
            
            <DemoStep
              number="6"
              title="Export & Share"
              description="Download as Excel or PDF, share with your team, or send directly to clients for approval."
              time="1 minute"
            />
          </div>
          
          <div className="text-center mt-16">
            <div className="inline-block bg-blue-50 px-8 py-4 rounded-lg">
              <p className="text-2xl font-bold text-blue-600">Total Time: 18-30 minutes</p>
              <p className="text-gray-600 mt-2">vs 20+ hours manually</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

function DemoStep({ number, title, description, time }: any) {
  return (
    <div className="flex gap-6 items-start">
      <div className="flex-shrink-0 w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold">
        {number}
      </div>
      <div className="flex-1">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-2xl font-bold">{title}</h3>
          <span className="text-sm text-blue-600 font-semibold bg-blue-50 px-3 py-1 rounded-full">
            {time}
          </span>
        </div>
        <p className="text-gray-600 text-lg">{description}</p>
      </div>
    </div>
  )
}

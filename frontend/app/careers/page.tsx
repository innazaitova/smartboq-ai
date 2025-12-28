import Link from 'next/link'

export default function CareersPage() {
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
          Join Our Team
        </h1>
        <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
          Help us transform the construction industry with AI. We're building the future of quantity surveying.
        </p>
      </section>

      {/* Why Join */}
      <section className="container mx-auto px-4 py-20">
        <h2 className="text-4xl font-bold text-center mb-16">Why Join QuantiBot AI?</h2>
        
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <Benefit
            emoji="🚀"
            title="High Impact"
            description="Your work directly impacts thousands of construction companies and millions in cost savings."
          />
          <Benefit
            emoji="🧠"
            title="Cutting Edge AI"
            description="Work with the latest AI models (GPT-4o, Claude) and shape the future of construction tech."
          />
          <Benefit
            emoji="🌍"
            title="Remote First"
            description="Work from anywhere. We're a distributed team across Pakistan, India, USA, and Europe."
          />
          <Benefit
            emoji="💰"
            title="Competitive Pay"
            description="Market-rate salaries, equity options, and performance bonuses."
          />
          <Benefit
            emoji="📈"
            title="Fast Growth"
            description="Join a rapidly growing startup. Shape the product and company culture."
          />
          <Benefit
            emoji="🎯"
            title="Meaningful Work"
            description="Build tools that make construction professionals' lives easier and businesses more profitable."
          />
        </div>
      </section>

      {/* Open Positions */}
      <section className="bg-white py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16">Open Positions</h2>
          
          <div className="max-w-4xl mx-auto space-y-6">
            <Position
              title="Senior AI/ML Engineer"
              location="Remote (Pakistan/India/Worldwide)"
              type="Full-time"
              description="Build and improve our AI models for construction drawing analysis. Experience with GPT-4, vision models, and Python required."
            />
            
            <Position
              title="Full Stack Developer"
              location="Remote (Pakistan/India/Worldwide)"
              type="Full-time"
              description="Build our web application with Next.js, React, FastAPI, and PostgreSQL. 3+ years experience required."
            />
            
            <Position
              title="Construction Domain Expert"
              location="Remote (Worldwide)"
              type="Full-time / Contract"
              description="Help train our AI models with quantity surveying expertise. 5+ years QS experience required."
            />
            
            <Position
              title="DevOps Engineer"
              location="Remote (Worldwide)"
              type="Full-time"
              description="Manage our infrastructure, CI/CD, and scaling. Experience with AWS, Docker, Kubernetes required."
            />
            
            <Position
              title="Product Designer"
              location="Remote (Worldwide)"
              type="Full-time"
              description="Design intuitive interfaces for construction professionals. Experience with Figma and user research required."
            />
          </div>
          
          <p className="text-center text-gray-600 mt-12">
            Don't see your role? Send us your resume at{' '}
            <a href="mailto:careers@quantibot.ai" className="text-blue-600 hover:underline">
              careers@quantibot.ai
            </a>
          </p>
        </div>
      </section>

      {/* Apply */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h2 className="text-4xl font-bold mb-6">Ready to Apply?</h2>
        <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
          Send your resume and a brief introduction to careers@quantibot.ai
        </p>
        <a 
          href="mailto:careers@quantibot.ai"
          className="bg-blue-600 text-white px-10 py-5 rounded-lg text-xl font-semibold hover:bg-blue-700 inline-block"
        >
          careers@quantibot.ai
        </a>
      </section>
    </div>
  )
}

function Benefit({ emoji, title, description }: any) {
  return (
    <div className="text-center p-6">
      <div className="text-5xl mb-4">{emoji}</div>
      <h3 className="text-xl font-bold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}

function Position({ title, location, type, description }: any) {
  return (
    <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-2xl font-bold mb-2">{title}</h3>
          <div className="flex gap-4 text-gray-600">
            <span>📍 {location}</span>
            <span>⏰ {type}</span>
          </div>
        </div>
      </div>
      <p className="text-gray-700 mb-4">{description}</p>
      <a 
        href="mailto:careers@quantibot.ai"
        className="text-blue-600 font-semibold hover:underline"
      >
        Apply Now →
      </a>
    </div>
  )
}

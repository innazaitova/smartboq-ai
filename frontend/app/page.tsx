// Landing Page
import Link from 'next/link'
import { ArrowRight, Check, Zap, DollarSign, Clock, Globe } from 'lucide-react'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex justify-between items-center">
          <div className="text-2xl font-bold text-blue-600">
            QuantiBot AI
          </div>
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

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-6xl font-bold text-gray-900 mb-6">
          Transform 20 Hours of Manual QS Work<br />
          into <span className="text-blue-600">30 Minutes</span>
        </h1>
        <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
          AI-Powered Quantity Surveying & Cost Estimation for Construction Projects.<br />
          Save 60-75% on QS costs. Get BOQ in minutes, not days.
        </p>
        <div className="flex gap-4 justify-center">
          <Link 
            href="/signup"
            className="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 flex items-center gap-2"
          >
            Start Free Trial <ArrowRight className="w-5 h-5" />
          </Link>
          <Link 
            href="/demo"
            className="border-2 border-blue-600 text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-50"
          >
            Watch Demo
          </Link>
        </div>
        <p className="text-sm text-gray-500 mt-4">
          No credit card required • 5 projects free • Cancel anytime
        </p>
      </section>

      {/* Benefits */}
      <section className="bg-white py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16">
            Why Construction Companies Love QuantiBot
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <BenefitCard 
              icon={<Clock className="w-12 h-12 text-blue-600" />}
              title="40x Faster"
              description="Generate complete BOQ in 30 minutes instead of 20 hours"
            />
            <BenefitCard 
              icon={<DollarSign className="w-12 h-12 text-blue-600" />}
              title="70% Cost Savings"
              description="$997/month vs $75,000/year for junior estimator"
            />
            <BenefitCard 
              icon={<Check className="w-12 h-12 text-blue-600" />}
              title="95%+ Accuracy"
              description="AI trained on thousands of projects. Continuous learning."
            />
            <BenefitCard 
              icon={<Globe className="w-12 h-12 text-blue-600" />}
              title="Global Coverage"
              description="Supports projects in 50+ countries. Multiple currencies."
            />
            <BenefitCard 
              icon={<Zap className="w-12 h-12 text-blue-600" />}
              title="Instant Updates"
              description="Design changed? Regenerate BOQ in minutes, not days."
            />
            <BenefitCard 
              icon={<Check className="w-12 h-12 text-blue-600" />}
              title="Code Compliant"
              description="IBC, Eurocode, IS Codes, BS Standards. Updated automatically."
            />
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16">
            How It Works
          </h2>
          <div className="grid md:grid-cols-4 gap-8">
            <StepCard 
              number="1"
              title="Upload Drawings"
              description="Upload PDF, DWG, or image files. Any format, any size."
            />
            <StepCard 
              number="2"
              title="AI Analyzes"
              description="Claude AI identifies every element with 95%+ accuracy."
            />
            <StepCard 
              number="3"
              title="Calculate Quantities"
              description="Automatic calculation compliant with local building codes."
            />
            <StepCard 
              number="4"
              title="Generate BOQ"
              description="Professional Bill of Quantities ready to submit."
            />
          </div>
          <p className="text-center text-2xl font-semibold mt-12 text-blue-600">
            Total Time: 30 minutes
            <span className="text-gray-500 text-lg ml-2">(vs 20 hours manual)</span>
          </p>
        </div>
      </section>

      {/* Social Proof */}
      <section className="bg-blue-600 text-white py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16">
            Trusted by Construction Companies Worldwide
          </h2>
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <StatCard number="5,000+" label="Projects Processed" />
            <StatCard number="95.7%" label="Accuracy Rate" />
            <StatCard number="$2.4M" label="Saved for Customers" />
            <StatCard number="18 min" label="Avg Processing Time" />
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">
            Ready to Transform Your Estimating Process?
          </h2>
          <p className="text-xl text-gray-600 mb-10">
            Join 500+ construction companies saving time and money with AI
          </p>
          <Link 
            href="/signup"
            className="bg-blue-600 text-white px-10 py-5 rounded-lg text-xl font-semibold hover:bg-blue-700 inline-flex items-center gap-2"
          >
            Start Free Trial - No Credit Card Required <ArrowRight className="w-6 h-6" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4">QuantiBot AI</h3>
              <p className="text-gray-400">
                AI-Powered Quantity Surveying & Cost Estimation
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/features">Features</Link></li>
                <li><Link href="/pricing">Pricing</Link></li>
                <li><Link href="/api">API</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/about">About</Link></li>
                <li><Link href="/contact">Contact</Link></li>
                <li><Link href="/careers">Careers</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/privacy">Privacy</Link></li>
                <li><Link href="/terms">Terms</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>© 2025 QuantiBot AI. All rights reserved.</p>
            <p className="mt-2">Built in Karachi 🇵🇰 | Serving the World 🌍</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

function BenefitCard({ icon, title, description }: any) {
  return (
    <div className="p-6 border rounded-lg hover:shadow-lg transition-shadow">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}

function StepCard({ number, title, description }: any) {
  return (
    <div className="text-center">
      <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
        {number}
      </div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}

function StatCard({ number, label }: any) {
  return (
    <div>
      <div className="text-5xl font-bold mb-2">{number}</div>
      <div className="text-blue-200">{label}</div>
    </div>
  )
}

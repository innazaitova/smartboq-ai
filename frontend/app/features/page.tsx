import Link from 'next/link'
import { ArrowRight, Check, Zap, Brain, FileText, Globe, Shield, TrendingUp, Users, Clock, DollarSign, BarChart } from 'lucide-react'

export default function FeaturesPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-blue-600">
            QuantiBot AI
          </Link>
          <div className="space-x-6">
            <Link href="/features" className="text-blue-600 font-semibold">
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
          Everything You Need to Estimate<br />
          <span className="text-blue-600">Faster, Better, Cheaper</span>
        </h1>
        <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
          QuantiBot AI combines cutting-edge artificial intelligence with industry expertise
          to deliver professional quantity surveying in minutes.
        </p>
      </section>

      {/* Core Features */}
      <section className="container mx-auto px-4 py-20">
        <h2 className="text-4xl font-bold text-center mb-16">Core Features</h2>
        
        <div className="grid md:grid-cols-2 gap-12 mb-20">
          <FeatureDetail
            icon={<Brain className="w-16 h-16 text-blue-600" />}
            title="AI-Powered Drawing Analysis"
            description="Our GPT-4o AI model analyzes your construction drawings with 95%+ accuracy, identifying every structural element, dimension, and specification."
            features={[
              "Supports PDF, DWG, DXF, and image formats",
              "Handles complex multi-page drawings",
              "Recognizes architectural, structural, and MEP elements",
              "Auto-detects scales and measurements"
            ]}
          />
          
          <FeatureDetail
            icon={<FileText className="w-16 h-16 text-blue-600" />}
            title="Automatic BOQ Generation"
            description="Professional Bill of Quantities generated instantly, formatted to industry standards and ready to submit to clients."
            features={[
              "IS 1200 standard format (customizable)",
              "Excel & PDF export",
              "Item-wise breakdown with units",
              "Cost estimation with material rates"
            ]}
          />

          <FeatureDetail
            icon={<Globe className="w-16 h-16 text-blue-600" />}
            title="Global Standards Compliance"
            description="Built-in support for international building codes and standards, automatically applied based on project location."
            features={[
              "IBC, Eurocode, IS Codes, BS Standards",
              "50+ countries supported",
              "Multi-currency cost calculation",
              "Local material rate databases"
            ]}
          />

          <FeatureDetail
            icon={<TrendingUp className="w-16 h-16 text-blue-600" />}
            title="Cost Estimation & Analytics"
            description="Real-time cost estimation with market rates, helping you bid more accurately and win more projects."
            features={[
              "Live material rates (updated daily)",
              "Labor cost calculation",
              "Overhead & profit margins",
              "Historical cost tracking"
            ]}
          />

          <FeatureDetail
            icon={<Zap className="w-16 h-16 text-blue-600" />}
            title="Lightning Fast Processing"
            description="What takes 20 hours manually takes 30 minutes with QuantiBot. Process multiple projects simultaneously."
            features={[
              "Average processing: 18 minutes",
              "Batch processing support",
              "Real-time progress tracking",
              "Priority processing for Pro plans"
            ]}
          />

          <FeatureDetail
            icon={<Shield className="w-16 h-16 text-blue-600" />}
            title="Enterprise Security"
            description="Bank-grade encryption and security measures to protect your sensitive project data."
            features={[
              "End-to-end encryption",
              "SOC 2 Type II compliant",
              "Regular security audits",
              "Role-based access control"
            ]}
          />
        </div>
      </section>

      {/* Additional Features */}
      <section className="bg-white py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16">Even More Features</h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <SmallFeature
              icon={<Users className="w-10 h-10 text-blue-600" />}
              title="Team Collaboration"
              description="Share projects with team members, assign tasks, and collaborate in real-time"
            />
            <SmallFeature
              icon={<Clock className="w-10 h-10 text-blue-600" />}
              title="Project Timeline"
              description="Automatic project scheduling and critical path analysis"
            />
            <SmallFeature
              icon={<BarChart className="w-10 h-10 text-blue-600" />}
              title="Custom Reports"
              description="Generate custom reports with your branding and specifications"
            />
            <SmallFeature
              icon={<FileText className="w-10 h-10 text-blue-600" />}
              title="Template Library"
              description="Pre-built templates for common construction types"
            />
            <SmallFeature
              icon={<DollarSign className="w-10 h-10 text-blue-600" />}
              title="Rate Analysis"
              description="Detailed rate analysis for all BOQ items"
            />
            <SmallFeature
              icon={<Check className="w-10 h-10 text-blue-600" />}
              title="Quality Checks"
              description="Automated quality checks and validation"
            />
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">
            Ready to Experience These Features?
          </h2>
          <p className="text-xl text-gray-600 mb-10">
            Start your free trial today - no credit card required
          </p>
          <Link 
            href="/signup"
            className="bg-blue-600 text-white px-10 py-5 rounded-lg text-xl font-semibold hover:bg-blue-700 inline-flex items-center gap-2"
          >
            Start Free Trial <ArrowRight className="w-6 h-6" />
          </Link>
        </div>
      </section>
    </div>
  )
}

function FeatureDetail({ icon, title, description, features }: any) {
  return (
    <div className="p-8 border rounded-xl hover:shadow-xl transition-shadow">
      <div className="mb-6">{icon}</div>
      <h3 className="text-2xl font-bold mb-4">{title}</h3>
      <p className="text-gray-600 mb-6">{description}</p>
      <ul className="space-y-3">
        {features.map((feature: string, index: number) => (
          <li key={index} className="flex items-start gap-3">
            <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-1" />
            <span className="text-gray-700">{feature}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

function SmallFeature({ icon, title, description }: any) {
  return (
    <div className="p-6 border rounded-lg hover:shadow-lg transition-shadow">
      <div className="mb-4">{icon}</div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-gray-600 text-sm">{description}</p>
    </div>
  )
}

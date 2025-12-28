import Link from 'next/link'

export default function AboutPage() {
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
          About QuantiBot AI
        </h1>
        <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
          We're on a mission to make professional quantity surveying accessible to every construction company, regardless of size or budget.
        </p>
      </section>

      {/* Story */}
      <section className="container mx-auto px-4 py-20">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-bold mb-8">Our Story</h2>
          <div className="prose prose-lg">
            <p className="text-gray-600 mb-6">
              QuantiBot AI was founded in 2024 in Karachi, Pakistan, by a team of construction engineers and AI experts who were frustrated with the time-consuming, error-prone process of manual quantity surveying.
            </p>
            <p className="text-gray-600 mb-6">
              We saw how small and medium-sized construction companies struggled to compete because they couldn't afford full-time quantity surveyors. Junior estimators cost $75,000/year, and projects would take 20+ hours to estimate manually.
            </p>
            <p className="text-gray-600 mb-6">
              With advances in AI, particularly GPT-4o's vision capabilities, we realized we could automate 95% of the quantity surveying process. What took days could now take minutes.
            </p>
            <p className="text-gray-600 mb-6">
              Today, QuantiBot AI serves construction companies in 50+ countries, processing thousands of projects monthly and saving millions of dollars in estimation costs.
            </p>
          </div>
        </div>
      </section>

      {/* Mission */}
      <section className="bg-white py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl font-bold mb-8">Our Mission</h2>
            <p className="text-2xl text-gray-700 leading-relaxed">
              To democratize professional quantity surveying by making it <span className="text-blue-600 font-semibold">40x faster</span>, <span className="text-blue-600 font-semibold">90% cheaper</span>, and accessible to every construction company worldwide.
            </p>
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="container mx-auto px-4 py-20">
        <h2 className="text-4xl font-bold text-center mb-16">Our Values</h2>
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <ValueCard
            title="Accuracy First"
            description="We obsess over accuracy. Our AI is trained on thousands of projects and achieves 95%+ accuracy on real-world drawings."
          />
          <ValueCard
            title="Customer Success"
            description="Your success is our success. We provide world-class support and continuously improve based on your feedback."
          />
          <ValueCard
            title="Innovation"
            description="We leverage cutting-edge AI technology to solve real construction problems and create genuine value."
          />
        </div>
      </section>

      {/* Team */}
      <section className="bg-white py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16">Our Team</h2>
          <p className="text-center text-gray-600 max-w-2xl mx-auto">
            We're a diverse team of construction engineers, AI researchers, and software developers from Pakistan, India, USA, and Europe, united by our passion for transforming the construction industry.
          </p>
        </div>
      </section>
    </div>
  )
}

function ValueCard({ title, description }: any) {
  return (
    <div className="p-6 border rounded-lg text-center hover:shadow-lg transition-shadow">
      <h3 className="text-xl font-bold mb-3">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}

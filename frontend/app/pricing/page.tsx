import Link from 'next/link'
import { ArrowRight, Check, X } from 'lucide-react'

export default function PricingPage() {
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
            <Link href="/pricing" className="text-blue-600 font-semibold">
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
          Simple, Transparent Pricing
        </h1>
        <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
          Save 60-75% compared to hiring a junior estimator ($75,000/year).<br />
          Choose the plan that fits your project volume.
        </p>
      </section>

      {/* Pricing Cards */}
      <section className="container mx-auto px-4 py-20">
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          
          {/* Trial Plan */}
          <PricingCard
            name="Trial"
            price="$0"
            period="forever"
            description="Perfect for testing QuantiBot"
            features={[
              { name: "5 projects", included: true },
              { name: "Basic BOQ generation", included: true },
              { name: "PDF & Excel export", included: true },
              { name: "Email support", included: true },
              { name: "Standard processing", included: true },
              { name: "Community support", included: true },
              { name: "Team collaboration", included: false },
              { name: "API access", included: false },
              { name: "Priority support", included: false }
            ]}
            ctaText="Start Free Trial"
            ctaLink="/signup"
            popular={false}
          />

          {/* Pro Plan */}
          <PricingCard
            name="Professional"
            price="$997"
            period="per month"
            description="For growing construction companies"
            features={[
              { name: "50 projects/month", included: true },
              { name: "Advanced BOQ generation", included: true },
              { name: "PDF & Excel export", included: true },
              { name: "Priority email support", included: true },
              { name: "Fast processing (2x speed)", included: true },
              { name: "5 team members", included: true },
              { name: "Custom templates", included: true },
              { name: "Rate analysis", included: true },
              { name: "API access (50 calls/day)", included: true }
            ]}
            ctaText="Start Professional"
            ctaLink="/signup?plan=pro"
            popular={true}
          />

          {/* Enterprise Plan */}
          <PricingCard
            name="Enterprise"
            price="Custom"
            period="contact us"
            description="For large organizations"
            features={[
              { name: "Unlimited projects", included: true },
              { name: "Enterprise BOQ features", included: true },
              { name: "All export formats", included: true },
              { name: "24/7 phone & email support", included: true },
              { name: "Fastest processing (5x speed)", included: true },
              { name: "Unlimited team members", included: true },
              { name: "Custom integrations", included: true },
              { name: "Dedicated account manager", included: true },
              { name: "Unlimited API access", included: true }
            ]}
            ctaText="Contact Sales"
            ctaLink="/contact"
            popular={false}
          />
        </div>
      </section>

      {/* Cost Comparison */}
      <section className="bg-white py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16">
            Cost Comparison: QuantiBot vs Traditional
          </h2>
          
          <div className="max-w-4xl mx-auto">
            <div className="grid md:grid-cols-2 gap-8">
              
              <div className="p-8 border-2 border-red-200 rounded-xl">
                <h3 className="text-2xl font-bold mb-6 text-red-600">Traditional Estimator</h3>
                <div className="space-y-4">
                  <CostItem label="Junior Estimator Salary" value="$75,000/year" />
                  <CostItem label="Benefits & Insurance" value="$15,000/year" />
                  <CostItem label="Software Licenses" value="$5,000/year" />
                  <CostItem label="Training & Development" value="$3,000/year" />
                  <CostItem label="Office Space & Equipment" value="$4,000/year" />
                  <div className="border-t-2 border-red-300 pt-4 mt-4">
                    <CostItem label="Total Annual Cost" value="$102,000" bold />
                  </div>
                  <div className="text-sm text-gray-600 mt-4">
                    • 20 hours per project<br />
                    • ~100 projects/year<br />
                    • Human errors possible
                  </div>
                </div>
              </div>

              <div className="p-8 border-2 border-green-500 rounded-xl bg-green-50">
                <h3 className="text-2xl font-bold mb-6 text-green-600">QuantiBot AI</h3>
                <div className="space-y-4">
                  <CostItem label="Professional Plan" value="$11,964/year" />
                  <CostItem label="Benefits & Insurance" value="$0" />
                  <CostItem label="Software Licenses" value="$0 (included)" />
                  <CostItem label="Training & Development" value="$0 (instant)" />
                  <CostItem label="Office Space & Equipment" value="$0" />
                  <div className="border-t-2 border-green-500 pt-4 mt-4">
                    <CostItem label="Total Annual Cost" value="$11,964" bold />
                  </div>
                  <div className="text-sm text-gray-600 mt-4">
                    • 30 minutes per project<br />
                    • 600 projects/year<br />
                    • 95%+ AI accuracy
                  </div>
                </div>
                <div className="mt-6 p-4 bg-green-600 text-white rounded-lg text-center">
                  <div className="text-3xl font-bold">88% Savings</div>
                  <div className="text-sm">Save $90,036 per year</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16">
            Frequently Asked Questions
          </h2>
          
          <div className="max-w-3xl mx-auto space-y-6">
            <FAQ
              question="Can I cancel anytime?"
              answer="Yes, absolutely. Cancel anytime with one click. No questions asked. You'll retain access until the end of your billing period."
            />
            <FAQ
              question="What payment methods do you accept?"
              answer="We accept all major credit cards (Visa, MasterCard, Amex), PayPal, and wire transfers for Enterprise plans."
            />
            <FAQ
              question="Is there a setup fee?"
              answer="No setup fees. No hidden costs. Just straightforward monthly pricing."
            />
            <FAQ
              question="What happens if I exceed my project limit?"
              answer="We'll notify you when you're near your limit. You can upgrade anytime or purchase additional project packs."
            />
            <FAQ
              question="Do you offer refunds?"
              answer="Yes, we offer a 30-day money-back guarantee. If you're not satisfied, we'll refund your payment in full."
            />
            <FAQ
              question="Can I switch plans later?"
              answer="Yes, upgrade or downgrade anytime. Changes take effect immediately, and we'll prorate the difference."
            />
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-blue-600 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">
            Ready to Save 88% on Estimating Costs?
          </h2>
          <p className="text-xl mb-10">
            Join 500+ construction companies already saving time and money
          </p>
          <Link 
            href="/signup"
            className="bg-white text-blue-600 px-10 py-5 rounded-lg text-xl font-semibold hover:bg-gray-100 inline-flex items-center gap-2"
          >
            Start Free Trial - 5 Projects Free <ArrowRight className="w-6 h-6" />
          </Link>
          <p className="text-sm mt-4 text-blue-100">
            No credit card required • Cancel anytime • Setup in 2 minutes
          </p>
        </div>
      </section>
    </div>
  )
}

function PricingCard({ name, price, period, description, features, ctaText, ctaLink, popular }: any) {
  return (
    <div className={`relative p-8 rounded-xl ${popular ? 'border-4 border-blue-600 shadow-2xl scale-105' : 'border-2 border-gray-200'}`}>
      {popular && (
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-blue-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
          Most Popular
        </div>
      )}
      
      <div className="text-center mb-8">
        <h3 className="text-2xl font-bold mb-2">{name}</h3>
        <div className="text-4xl font-bold text-blue-600 mb-2">{price}</div>
        <div className="text-gray-600">{period}</div>
        <p className="text-gray-600 mt-4">{description}</p>
      </div>
      
      <ul className="space-y-4 mb-8">
        {features.map((feature: any, index: number) => (
          <li key={index} className="flex items-start gap-3">
            {feature.included ? (
              <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
            ) : (
              <X className="w-5 h-5 text-gray-300 flex-shrink-0 mt-0.5" />
            )}
            <span className={feature.included ? 'text-gray-700' : 'text-gray-400'}>
              {feature.name}
            </span>
          </li>
        ))}
      </ul>
      
      <Link
        href={ctaLink}
        className={`block text-center py-3 px-6 rounded-lg font-semibold ${
          popular
            ? 'bg-blue-600 text-white hover:bg-blue-700'
            : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
        }`}
      >
        {ctaText}
      </Link>
    </div>
  )
}

function CostItem({ label, value, bold }: any) {
  return (
    <div className={`flex justify-between ${bold ? 'font-bold text-lg' : ''}`}>
      <span>{label}</span>
      <span>{value}</span>
    </div>
  )
}

function FAQ({ question, answer }: any) {
  return (
    <div className="border rounded-lg p-6">
      <h3 className="text-xl font-semibold mb-3">{question}</h3>
      <p className="text-gray-600">{answer}</p>
    </div>
  )
}

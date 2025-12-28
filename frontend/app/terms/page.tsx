import Link from 'next/link'

export default function TermsPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="container mx-auto px-4 py-6 border-b">
        <nav className="flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-blue-600">
            QuantiBot AI
          </Link>
          <Link href="/" className="text-gray-600 hover:text-gray-900">
            ← Back to Home
          </Link>
        </nav>
      </header>

      {/* Content */}
      <div className="container mx-auto px-4 py-20 max-w-4xl">
        <h1 className="text-5xl font-bold mb-4">Terms of Service</h1>
        <p className="text-gray-600 mb-12">Last updated: December 28, 2025</p>

        <div className="prose prose-lg max-w-none">
          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">1. Acceptance of Terms</h2>
            <p className="text-gray-700 mb-4">
              By accessing and using QuantiBot AI ("Service"), you accept and agree to be bound by these Terms of Service. If you do not agree, do not use the Service.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">2. Description of Service</h2>
            <p className="text-gray-700 mb-4">
              QuantiBot AI provides AI-powered quantity surveying and cost estimation services for construction projects. We use artificial intelligence to analyze construction drawings and generate Bills of Quantities (BOQ).
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">3. Account Registration</h2>
            <p className="text-gray-700 mb-4">You must:</p>
            <ul className="list-disc pl-6 space-y-2 text-gray-700">
              <li>Be at least 18 years old</li>
              <li>Provide accurate and complete registration information</li>
              <li>Maintain the security of your account credentials</li>
              <li>Notify us immediately of any unauthorized access</li>
              <li>Be responsible for all activities under your account</li>
            </ul>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">4. Subscription Plans</h2>
            
            <h3 className="text-2xl font-semibold mb-3 mt-6">Trial Plan</h3>
            <p className="text-gray-700 mb-4">
              Free trial includes 5 projects. No credit card required. Limited to one trial per user/company.
            </p>

            <h3 className="text-2xl font-semibold mb-3 mt-6">Professional Plan</h3>
            <p className="text-gray-700 mb-4">
              $997/month, billed monthly. Includes 50 projects/month. Cancel anytime.
            </p>

            <h3 className="text-2xl font-semibold mb-3 mt-6">Enterprise Plan</h3>
            <p className="text-gray-700 mb-4">
              Custom pricing. Contact sales for details. Custom contract terms apply.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">5. Payment Terms</h2>
            <ul className="list-disc pl-6 space-y-2 text-gray-700">
              <li>Payments are processed monthly in advance</li>
              <li>All fees are in USD unless otherwise specified</li>
              <li>Failed payments may result in service suspension</li>
              <li>No refunds for partial months</li>
              <li>30-day money-back guarantee for first payment</li>
            </ul>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">6. Acceptable Use</h2>
            <p className="text-gray-700 mb-4">You may NOT:</p>
            <ul className="list-disc pl-6 space-y-2 text-gray-700">
              <li>Use the Service for illegal purposes</li>
              <li>Attempt to reverse engineer or copy our AI models</li>
              <li>Share your account with others</li>
              <li>Upload malicious files or viruses</li>
              <li>Abuse or overload our systems</li>
              <li>Resell or redistribute our Service without permission</li>
              <li>Use the Service to compete with us</li>
            </ul>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">7. Intellectual Property</h2>
            <p className="text-gray-700 mb-4">
              You retain all rights to your construction drawings and project data. We retain all rights to our AI models, software, and Service. By using the Service, you grant us a license to process your data solely to provide the Service.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">8. AI Accuracy Disclaimer</h2>
            <p className="text-gray-700 mb-4">
              While our AI achieves 95%+ accuracy, QuantiBot AI is a tool to assist professionals, not replace them. You are responsible for:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-gray-700">
              <li>Reviewing all AI-generated outputs</li>
              <li>Verifying quantities and calculations</li>
              <li>Ensuring compliance with local codes</li>
              <li>Final approval of all BOQs and estimates</li>
            </ul>
            <p className="text-gray-700 mt-4">
              <strong>WE PROVIDE THE SERVICE "AS IS" WITHOUT WARRANTIES OF ANY KIND.</strong>
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">9. Limitation of Liability</h2>
            <p className="text-gray-700 mb-4">
              TO THE MAXIMUM EXTENT PERMITTED BY LAW:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-gray-700">
              <li>We are not liable for any indirect, incidental, or consequential damages</li>
              <li>Our total liability is limited to fees paid in the last 12 months</li>
              <li>We are not responsible for errors in AI-generated outputs</li>
              <li>You use the Service at your own risk</li>
            </ul>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">10. Data Ownership and Usage</h2>
            <p className="text-gray-700 mb-4">
              Your data remains yours. We may use anonymized, aggregated data to improve our AI models. See our Privacy Policy for details.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">11. Termination</h2>
            <p className="text-gray-700 mb-4">
              Either party may terminate at any time. Upon termination:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-gray-700">
              <li>Your access to the Service will cease</li>
              <li>You can export your data within 30 days</li>
              <li>We will delete your data after 30 days</li>
              <li>No refunds for remaining subscription period (except money-back guarantee)</li>
            </ul>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">12. Changes to Terms</h2>
            <p className="text-gray-700 mb-4">
              We may modify these Terms at any time. Continued use after changes constitutes acceptance. We will notify you of material changes via email.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">13. Governing Law</h2>
            <p className="text-gray-700 mb-4">
              These Terms are governed by the laws of Pakistan. Disputes shall be resolved through arbitration in Karachi.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">14. Contact</h2>
            <p className="text-gray-700 mb-4">
              For questions about these Terms:<br />
              Email: legal@quantibot.ai<br />
              Address: Karachi, Pakistan
            </p>
          </section>
        </div>
      </div>
    </div>
  )
}

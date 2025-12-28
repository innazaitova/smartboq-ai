import Link from 'next/link'

export default function PrivacyPage() {
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
        <h1 className="text-5xl font-bold mb-4">Privacy Policy</h1>
        <p className="text-gray-600 mb-12">Last updated: December 28, 2025</p>

        <div className="prose prose-lg max-w-none">
          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Introduction</h2>
            <p className="text-gray-700 mb-4">
              QuantiBot AI ("we," "our," or "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our service.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Information We Collect</h2>
            
            <h3 className="text-2xl font-semibold mb-3 mt-6">Account Information</h3>
            <p className="text-gray-700 mb-4">
              When you create an account, we collect your name, email address, company name, and password (encrypted).
            </p>

            <h3 className="text-2xl font-semibold mb-3 mt-6">Project Data</h3>
            <p className="text-gray-700 mb-4">
              We collect and process construction drawings, project details, BOQ data, and related files you upload to our platform.
            </p>

            <h3 className="text-2xl font-semibold mb-3 mt-6">Usage Data</h3>
            <p className="text-gray-700 mb-4">
              We automatically collect information about how you interact with our service, including IP address, browser type, pages visited, and time spent on the platform.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">How We Use Your Information</h2>
            <ul className="list-disc pl-6 space-y-2 text-gray-700">
              <li>To provide and maintain our AI-powered quantity surveying service</li>
              <li>To process your construction drawings and generate BOQs</li>
              <li>To improve our AI models and service quality</li>
              <li>To communicate with you about your account and projects</li>
              <li>To provide customer support</li>
              <li>To detect and prevent fraud or abuse</li>
              <li>To comply with legal obligations</li>
            </ul>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Data Security</h2>
            <p className="text-gray-700 mb-4">
              We implement industry-standard security measures to protect your data:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-gray-700">
              <li>End-to-end encryption for all data in transit</li>
              <li>AES-256 encryption for data at rest</li>
              <li>Regular security audits and penetration testing</li>
              <li>SOC 2 Type II compliance</li>
              <li>Role-based access controls</li>
            </ul>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Data Sharing</h2>
            <p className="text-gray-700 mb-4">
              We do not sell your personal information. We may share data with:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-gray-700">
              <li><strong>AI Providers:</strong> OpenAI for processing drawings (covered by their enterprise privacy agreement)</li>
              <li><strong>Cloud Services:</strong> AWS for hosting and storage</li>
              <li><strong>Analytics:</strong> Anonymized usage data for service improvement</li>
              <li><strong>Legal Requirements:</strong> When required by law</li>
            </ul>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Your Rights</h2>
            <p className="text-gray-700 mb-4">You have the right to:</p>
            <ul className="list-disc pl-6 space-y-2 text-gray-700">
              <li>Access your personal data</li>
              <li>Correct inaccurate data</li>
              <li>Request deletion of your data</li>
              <li>Export your data</li>
              <li>Opt out of marketing communications</li>
              <li>Withdraw consent at any time</li>
            </ul>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Data Retention</h2>
            <p className="text-gray-700 mb-4">
              We retain your data for as long as your account is active. After account deletion, we securely delete all personal data within 30 days, except where required by law.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Cookies</h2>
            <p className="text-gray-700 mb-4">
              We use essential cookies for authentication and service functionality. We do not use third-party advertising cookies.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Children's Privacy</h2>
            <p className="text-gray-700 mb-4">
              Our service is not intended for users under 18. We do not knowingly collect data from children.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Changes to This Policy</h2>
            <p className="text-gray-700 mb-4">
              We may update this Privacy Policy from time to time. We will notify you of significant changes via email.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Contact Us</h2>
            <p className="text-gray-700 mb-4">
              If you have questions about this Privacy Policy, contact us at:
            </p>
            <p className="text-gray-700">
              Email: privacy@quantibot.ai<br />
              Address: Karachi, Pakistan
            </p>
          </section>
        </div>
      </div>
    </div>
  )
}

import React from 'react'

export default function PrivacyPage() {
  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 text-white py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Privacy Policy
            </h1>
            <p className="text-xl md:text-2xl text-primary-100 mb-8 max-w-3xl mx-auto">
              Your privacy is important to us. Learn how we collect, use, and protect your data.
            </p>
            <p className="text-lg text-primary-200">
              Last updated: December 2024
            </p>
          </div>
        </div>
      </section>

      {/* Privacy Policy Content */}
      <section className="bg-white py-24">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div className="prose prose-lg max-w-none">
            
            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">1. Information We Collect</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  <strong>Personal Information:</strong> When you register for our service, we collect your name, email address, company information, and contact details.
                </p>
                <p>
                  <strong>Usage Data:</strong> We automatically collect information about how you use our platform, including search queries, application data, and interaction patterns.
                </p>
                <p>
                  <strong>Technical Data:</strong> We collect IP addresses, browser types, device information, and other technical identifiers to provide and improve our services.
                </p>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">2. How We Use Your Information</h2>
              <div className="space-y-4 text-gray-600">
                <p>We use the collected information to:</p>
                <ul className="list-disc list-inside space-y-2 ml-4">
                  <li>Provide and maintain our grant discovery and application services</li>
                  <li>Send you relevant grant opportunities and platform updates</li>
                  <li>Improve our AI algorithms and matching capabilities</li>
                  <li>Provide customer support and respond to your inquiries</li>
                  <li>Ensure platform security and prevent fraud</li>
                  <li>Comply with legal obligations and regulatory requirements</li>
                </ul>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">3. Legal Basis for Processing (GDPR)</h2>
              <div className="space-y-4 text-gray-600">
                <p>We process your personal data based on:</p>
                <ul className="list-disc list-inside space-y-2 ml-4">
                  <li><strong>Contract:</strong> To provide services as outlined in our Terms of Service</li>
                  <li><strong>Legitimate Interest:</strong> To improve our platform and provide relevant recommendations</li>
                  <li><strong>Consent:</strong> For marketing communications and optional features</li>
                  <li><strong>Legal Obligation:</strong> To comply with EU and member state regulations</li>
                </ul>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">4. Data Sharing and Disclosure</h2>
              <div className="space-y-4 text-gray-600">
                <p>We may share your information with:</p>
                <ul className="list-disc list-inside space-y-2 ml-4">
                  <li><strong>Service Providers:</strong> Trusted partners who assist in providing our services</li>
                  <li><strong>EU Institutions:</strong> When required for grant application processing (with your consent)</li>
                  <li><strong>Legal Authorities:</strong> When required by law or to protect our rights</li>
                </ul>
                <p>
                  We never sell your personal data to third parties for marketing purposes.
                </p>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">5. Your Rights Under GDPR</h2>
              <div className="space-y-4 text-gray-600">
                <p>You have the following rights regarding your personal data:</p>
                <ul className="list-disc list-inside space-y-2 ml-4">
                  <li><strong>Access:</strong> Request a copy of your personal data</li>
                  <li><strong>Rectification:</strong> Correct inaccurate or incomplete data</li>
                  <li><strong>Erasure:</strong> Request deletion of your data (right to be forgotten)</li>
                  <li><strong>Portability:</strong> Receive your data in a portable format</li>
                  <li><strong>Restriction:</strong> Limit how we process your data</li>
                  <li><strong>Objection:</strong> Object to processing based on legitimate interests</li>
                  <li><strong>Withdraw Consent:</strong> Withdraw consent for consent-based processing</li>
                </ul>
                <p>
                  To exercise these rights, contact us at <a href="mailto:privacy@eugrantsmonitor.com" className="text-primary-600 hover:text-primary-700">privacy@eugrantsmonitor.com</a>.
                </p>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">6. Data Security</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  We implement appropriate technical and organizational measures to protect your data, including:
                </p>
                <ul className="list-disc list-inside space-y-2 ml-4">
                  <li>End-to-end encryption for data transmission</li>
                  <li>Secure data centers within the EU</li>
                  <li>Regular security audits and penetration testing</li>
                  <li>Access controls and staff training</li>
                  <li>Data backup and disaster recovery procedures</li>
                </ul>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">7. Data Retention</h2>
              <div className="space-y-4 text-gray-600">
                <p>We retain your personal data only for as long as necessary to:</p>
                <ul className="list-disc list-inside space-y-2 ml-4">
                  <li>Provide our services while you have an active account</li>
                  <li>Comply with legal, accounting, or reporting requirements</li>
                  <li>Resolve disputes and enforce our agreements</li>
                </ul>
                <p>
                  Account data is deleted within 30 days of account closure, unless longer retention is required by law.
                </p>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">8. International Transfers</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  Your data is primarily processed within the European Economic Area (EEA). 
                  Any transfers to countries outside the EEA are protected by appropriate safeguards, 
                  including EU Standard Contractual Clauses.
                </p>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">9. Cookies and Tracking</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  We use necessary cookies for platform functionality and, with your consent, 
                  analytics cookies to improve our services. You can manage cookie preferences 
                  in your browser settings or through our cookie banner.
                </p>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">10. Children's Privacy</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  Our services are not intended for individuals under 16 years of age. 
                  We do not knowingly collect personal data from children under 16.
                </p>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">11. Changes to This Policy</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  We may update this Privacy Policy periodically. We will notify you of significant 
                  changes via email or through our platform. Continued use of our services after 
                  changes constitutes acceptance of the updated policy.
                </p>
              </div>
            </div>

            <div className="card">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">12. Contact Information</h2>
              <div className="space-y-4 text-gray-600">
                <p><strong>Data Controller:</strong> EU Grants Monitor</p>
                <p><strong>Address:</strong> European Quarter, 1000 Brussels, Belgium</p>
                <p><strong>Email:</strong> <a href="mailto:privacy@eugrantsmonitor.com" className="text-primary-600 hover:text-primary-700">privacy@eugrantsmonitor.com</a></p>
                <p><strong>DPO:</strong> <a href="mailto:dpo@eugrantsmonitor.com" className="text-primary-600 hover:text-primary-700">dpo@eugrantsmonitor.com</a></p>
                <p>
                  <strong>Supervisory Authority:</strong> You have the right to lodge a complaint with 
                  your local data protection authority if you believe we have not addressed your concerns adequately.
                </p>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gray-50 py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Questions About Your Privacy?
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Our privacy team is here to help you understand your rights and how we protect your data.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/contact" className="btn btn-primary text-lg px-8 py-3">
              Contact Privacy Team
            </a>
            <a href="/help" className="btn btn-outline text-lg px-8 py-3">
              Visit Help Center
            </a>
          </div>
        </div>
      </section>
    </div>
  )
}

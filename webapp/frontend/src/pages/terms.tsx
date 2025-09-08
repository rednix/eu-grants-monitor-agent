import React from 'react'

export default function TermsPage() {
  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 text-white py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Terms of Service
            </h1>
            <p className="text-xl md:text-2xl text-primary-100 mb-8 max-w-3xl mx-auto">
              Please read these terms carefully before using our platform.
            </p>
            <p className="text-lg text-primary-200">
              Last updated: December 2024
            </p>
          </div>
        </div>
      </section>

      {/* Terms Content */}
      <section className="bg-white py-24">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div className="prose prose-lg max-w-none">
            
            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">1. Agreement to Terms</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  By accessing and using EU Grants Monitor ("Service"), you accept and agree to be bound by the terms 
                  and provision of this agreement. If you do not agree to abide by the above, please do not use this service.
                </p>
                <p>
                  These Terms of Service constitute a legally binding agreement between you and EU Grants Monitor 
                  ("Company", "we", "us", or "our").
                </p>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">2. Description of Service</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  EU Grants Monitor provides an AI-powered platform for discovering, analyzing, and applying for 
                  European Union funding opportunities. Our services include:
                </p>
                <ul className="list-disc list-inside space-y-2 ml-4">
                  <li>Grant database access and search functionality</li>
                  <li>AI-powered application assistance and optimization</li>
                  <li>Analytics and reporting tools</li>
                  <li>Document management and collaboration features</li>
                  <li>API access for integration (Enterprise plans)</li>
                </ul>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">3. Account Registration and Eligibility</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  <strong>Eligibility:</strong> You must be at least 18 years old and legally capable of entering 
                  into binding contracts to use our Service.
                </p>
                <p>
                  <strong>Account Security:</strong> You are responsible for maintaining the confidentiality of your 
                  account credentials and for all activities that occur under your account.
                </p>
                <p>
                  <strong>Accurate Information:</strong> You agree to provide accurate, complete, and current information 
                  during registration and to update such information to keep it accurate and complete.
                </p>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">4. Subscription Plans and Billing</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  <strong>Subscription Plans:</strong> We offer various subscription plans with different features and limits. 
                  Details are available on our pricing page.
                </p>
                <p>
                  <strong>Billing:</strong> Subscription fees are billed in advance on a monthly or yearly basis. 
                  All fees are non-refundable except as required by law.
                </p>
                <p>
                  <strong>Automatic Renewal:</strong> Subscriptions automatically renew unless cancelled before the 
                  end of the current billing period.
                </p>
                <p>
                  <strong>Price Changes:</strong> We may change subscription fees with 30 days' notice. 
                  Changes apply to subsequent billing periods.
                </p>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">5. Acceptable Use Policy</h2>
              <div className="space-y-4 text-gray-600">
                <p>You agree not to:</p>
                <ul className="list-disc list-inside space-y-2 ml-4">
                  <li>Use the Service for any unlawful purpose or in violation of any applicable laws</li>
                  <li>Share your account credentials with others</li>
                  <li>Attempt to gain unauthorized access to our systems or other users' accounts</li>
                  <li>Use automated tools to scrape or collect data from our platform</li>
                  <li>Submit false or misleading information in grant applications</li>
                  <li>Interfere with or disrupt the integrity or performance of our Service</li>
                  <li>Violate any applicable export control laws</li>
                </ul>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">6. Intellectual Property</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  <strong>Our Content:</strong> All content, features, and functionality of our Service, including but not 
                  limited to text, graphics, logos, software, and AI algorithms, are owned by us and are protected by 
                  copyright, trademark, and other intellectual property laws.
                </p>
                <p>
                  <strong>Your Content:</strong> You retain ownership of any content you upload or create using our Service. 
                  You grant us a license to use, store, and process your content to provide our services.
                </p>
                <p>
                  <strong>Feedback:</strong> Any feedback, suggestions, or ideas you provide to us become our property 
                  and may be used without compensation or attribution.
                </p>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">7. Data and Privacy</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  Our collection, use, and protection of your personal data is governed by our Privacy Policy, 
                  which is incorporated into these Terms by reference. By using our Service, you consent to 
                  our data practices as described in the Privacy Policy.
                </p>
                <p>
                  We comply with applicable data protection laws, including the General Data Protection Regulation (GDPR) 
                  for EU users.
                </p>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">8. Service Availability and Support</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  <strong>Availability:</strong> While we strive for high availability, we do not guarantee that our 
                  Service will be available 100% of the time. We may perform maintenance or updates that temporarily 
                  affect service availability.
                </p>
                <p>
                  <strong>Support:</strong> Support levels vary by subscription plan. We provide email support for all 
                  users, with additional support channels available for higher-tier plans.
                </p>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">9. Disclaimers and Limitations of Liability</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  <strong>No Warranty:</strong> Our Service is provided "as is" without any warranties, express or implied. 
                  We disclaim all warranties including merchantability, fitness for a particular purpose, and non-infringement.
                </p>
                <p>
                  <strong>Grant Applications:</strong> We provide tools and assistance for grant applications, but we do not 
                  guarantee approval or funding. Success depends on many factors beyond our control.
                </p>
                <p>
                  <strong>Limitation of Liability:</strong> To the maximum extent permitted by law, our liability for any 
                  damages arising from your use of our Service is limited to the amount you paid for the Service in the 
                  12 months preceding the event giving rise to liability.
                </p>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">10. Termination</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  <strong>By You:</strong> You may cancel your subscription at any time through your account settings. 
                  Cancellation takes effect at the end of the current billing period.
                </p>
                <p>
                  <strong>By Us:</strong> We may suspend or terminate your account if you violate these Terms or for other 
                  reasons at our discretion, with or without notice.
                </p>
                <p>
                  <strong>Effect of Termination:</strong> Upon termination, your right to use the Service ceases immediately. 
                  We may delete your data after account closure, subject to our Privacy Policy and legal requirements.
                </p>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">11. Changes to Terms</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  We reserve the right to modify these Terms at any time. We will notify users of material changes 
                  via email or through our platform. Continued use of the Service after changes constitutes acceptance 
                  of the new Terms.
                </p>
              </div>
            </div>

            <div className="card mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">12. Governing Law and Disputes</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  These Terms are governed by the laws of Belgium. Any disputes arising from these Terms or your use 
                  of our Service shall be resolved in the courts of Brussels, Belgium.
                </p>
                <p>
                  For EU consumers, this does not affect your statutory rights or your right to bring proceedings 
                  in your country of residence.
                </p>
              </div>
            </div>

            <div className="card">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">13. Contact Information</h2>
              <div className="space-y-4 text-gray-600">
                <p><strong>Company:</strong> EU Grants Monitor</p>
                <p><strong>Address:</strong> European Quarter, 1000 Brussels, Belgium</p>
                <p><strong>Email:</strong> <a href="mailto:legal@eugrantsmonitor.com" className="text-primary-600 hover:text-primary-700">legal@eugrantsmonitor.com</a></p>
                <p><strong>Support:</strong> <a href="mailto:support@eugrantsmonitor.com" className="text-primary-600 hover:text-primary-700">support@eugrantsmonitor.com</a></p>
                <p>
                  If you have any questions about these Terms, please contact us using the information above.
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
            Questions About Our Terms?
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Our legal team is available to clarify any aspects of our Terms of Service.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/contact" className="btn btn-primary text-lg px-8 py-3">
              Contact Legal Team
            </a>
            <a href="/privacy" className="btn btn-outline text-lg px-8 py-3">
              View Privacy Policy
            </a>
          </div>
        </div>
      </section>
    </div>
  )
}

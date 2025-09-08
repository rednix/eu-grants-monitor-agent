import React, { useState } from 'react'
import { CheckIcon, XMarkIcon } from '@heroicons/react/24/outline'

export default function PricingPage() {
  const [isYearly, setIsYearly] = useState(false)

  const plans = [
    {
      name: 'Starter',
      description: 'Perfect for small businesses exploring EU funding opportunities',
      monthlyPrice: 29,
      yearlyPrice: 290,
      features: [
        'Access to all EU grant opportunities',
        'Basic search and filtering',
        'Up to 5 saved searches',
        'Email alerts for new opportunities',
        'Basic application templates',
        'Community support'
      ],
      limitations: [
        'Limited to 10 applications per month',
        'Basic analytics only'
      ],
      popular: false,
      cta: 'Start Free Trial'
    },
    {
      name: 'Professional',
      description: 'Ideal for growing companies with active grant strategies',
      monthlyPrice: 89,
      yearlyPrice: 890,
      features: [
        'Everything in Starter',
        'AI-powered application assistance',
        'Unlimited saved searches',
        'Advanced analytics and reporting',
        'Priority email support',
        'Document templates library',
        'Success rate optimization',
        'Collaboration tools for teams'
      ],
      limitations: [
        'Limited to 50 applications per month'
      ],
      popular: true,
      cta: 'Start Free Trial'
    },
    {
      name: 'Enterprise',
      description: 'For large organizations with complex funding needs',
      monthlyPrice: 249,
      yearlyPrice: 2490,
      features: [
        'Everything in Professional',
        'Unlimited applications',
        'Custom integrations via API',
        'Dedicated account manager',
        'White-label options',
        'Advanced compliance checking',
        'Custom reporting and dashboards',
        'Phone and priority support',
        'Training and onboarding'
      ],
      limitations: [],
      popular: false,
      cta: 'Contact Sales'
    }
  ]

  const faqs = [
    {
      question: 'What is included in the free trial?',
      answer: 'The free trial gives you full access to your chosen plan for 14 days, including all features and support. No credit card required to start.'
    },
    {
      question: 'Can I change plans anytime?',
      answer: 'Yes, you can upgrade or downgrade your plan at any time. Changes take effect immediately, and we\'ll prorate any billing adjustments.'
    },
    {
      question: 'What payment methods do you accept?',
      answer: 'We accept all major credit cards, bank transfers, and can accommodate other payment methods for Enterprise customers.'
    },
    {
      question: 'Is there a setup fee?',
      answer: 'No, there are no setup fees for any of our plans. You only pay the monthly or yearly subscription cost.'
    },
    {
      question: 'Do you offer discounts for non-profits?',
      answer: 'Yes, we offer special pricing for registered non-profit organizations. Contact our sales team for more information.'
    },
    {
      question: 'What happens if I exceed my application limit?',
      answer: 'We\'ll notify you when you\'re approaching your limit. You can either upgrade your plan or purchase additional applications as needed.'
    }
  ]

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 text-white py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Simple, Transparent
              <br />
              <span className="text-primary-200">Pricing</span>
            </h1>
            <p className="text-xl md:text-2xl text-primary-100 mb-8 max-w-3xl mx-auto">
              Choose the perfect plan for your grant funding journey. All plans include our core AI-powered features.
            </p>
            
            {/* Billing Toggle */}
            <div className="flex items-center justify-center space-x-4 mb-8">
              <span className={`text-lg ${!isYearly ? 'text-white font-semibold' : 'text-primary-200'}`}>
                Monthly
              </span>
              <button
                onClick={() => setIsYearly(!isYearly)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  isYearly ? 'bg-primary-200' : 'bg-primary-400'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    isYearly ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
              <span className={`text-lg ${isYearly ? 'text-white font-semibold' : 'text-primary-200'}`}>
                Yearly
                <span className="ml-2 text-sm bg-green-500 text-white px-2 py-1 rounded-full">
                  Save 20%
                </span>
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Plans */}
      <section className="bg-white py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {plans.map((plan) => (
              <div
                key={plan.name}
                className={`card relative ${
                  plan.popular ? 'border-2 border-primary-500 shadow-xl scale-105' : 'border border-gray-200'
                }`}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-primary-500 text-white px-4 py-2 rounded-full text-sm font-semibold">
                      Most Popular
                    </span>
                  </div>
                )}
                
                <div className="text-center mb-6">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                  <p className="text-gray-600 mb-4">{plan.description}</p>
                  <div className="mb-4">
                    <span className="text-4xl font-bold text-gray-900">
                      €{isYearly ? plan.yearlyPrice : plan.monthlyPrice}
                    </span>
                    <span className="text-gray-600 ml-2">
                      {isYearly ? '/year' : '/month'}
                    </span>
                  </div>
                  {isYearly && (
                    <p className="text-sm text-green-600 font-medium">
                      Save €{(plan.monthlyPrice * 12) - plan.yearlyPrice} per year
                    </p>
                  )}
                </div>

                <div className="mb-6">
                  <h4 className="font-semibold text-gray-900 mb-3">What's included:</h4>
                  <ul className="space-y-2">
                    {plan.features.map((feature) => (
                      <li key={feature} className="flex items-start">
                        <CheckIcon className="h-5 w-5 text-green-500 mt-0.5 mr-2 flex-shrink-0" />
                        <span className="text-gray-700 text-sm">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {plan.limitations.length > 0 && (
                  <div className="mb-6">
                    <h4 className="font-semibold text-gray-900 mb-3">Limitations:</h4>
                    <ul className="space-y-2">
                      {plan.limitations.map((limitation) => (
                        <li key={limitation} className="flex items-start">
                          <XMarkIcon className="h-5 w-5 text-gray-400 mt-0.5 mr-2 flex-shrink-0" />
                          <span className="text-gray-600 text-sm">{limitation}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                <button
                  className={`btn w-full ${
                    plan.popular
                      ? 'btn-primary'
                      : 'btn-outline hover:bg-primary-50 hover:border-primary-300'
                  }`}
                >
                  {plan.cta}
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Comparison */}
      <section className="bg-gray-50 py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Compare All Features
            </h2>
            <p className="text-xl text-gray-600">
              See exactly what's included in each plan
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full bg-white rounded-lg shadow-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-4 px-6 font-semibold text-gray-900">Features</th>
                  <th className="text-center py-4 px-6 font-semibold text-gray-900">Starter</th>
                  <th className="text-center py-4 px-6 font-semibold text-gray-900">Professional</th>
                  <th className="text-center py-4 px-6 font-semibold text-gray-900">Enterprise</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                <tr>
                  <td className="py-4 px-6 text-gray-900">Grant Database Access</td>
                  <td className="py-4 px-6 text-center"><CheckIcon className="h-5 w-5 text-green-500 mx-auto" /></td>
                  <td className="py-4 px-6 text-center"><CheckIcon className="h-5 w-5 text-green-500 mx-auto" /></td>
                  <td className="py-4 px-6 text-center"><CheckIcon className="h-5 w-5 text-green-500 mx-auto" /></td>
                </tr>
                <tr>
                  <td className="py-4 px-6 text-gray-900">AI Application Assistant</td>
                  <td className="py-4 px-6 text-center"><XMarkIcon className="h-5 w-5 text-gray-400 mx-auto" /></td>
                  <td className="py-4 px-6 text-center"><CheckIcon className="h-5 w-5 text-green-500 mx-auto" /></td>
                  <td className="py-4 px-6 text-center"><CheckIcon className="h-5 w-5 text-green-500 mx-auto" /></td>
                </tr>
                <tr>
                  <td className="py-4 px-6 text-gray-900">Advanced Analytics</td>
                  <td className="py-4 px-6 text-center"><XMarkIcon className="h-5 w-5 text-gray-400 mx-auto" /></td>
                  <td className="py-4 px-6 text-center"><CheckIcon className="h-5 w-5 text-green-500 mx-auto" /></td>
                  <td className="py-4 px-6 text-center"><CheckIcon className="h-5 w-5 text-green-500 mx-auto" /></td>
                </tr>
                <tr>
                  <td className="py-4 px-6 text-gray-900">API Access</td>
                  <td className="py-4 px-6 text-center"><XMarkIcon className="h-5 w-5 text-gray-400 mx-auto" /></td>
                  <td className="py-4 px-6 text-center"><XMarkIcon className="h-5 w-5 text-gray-400 mx-auto" /></td>
                  <td className="py-4 px-6 text-center"><CheckIcon className="h-5 w-5 text-green-500 mx-auto" /></td>
                </tr>
                <tr>
                  <td className="py-4 px-6 text-gray-900">Dedicated Account Manager</td>
                  <td className="py-4 px-6 text-center"><XMarkIcon className="h-5 w-5 text-gray-400 mx-auto" /></td>
                  <td className="py-4 px-6 text-center"><XMarkIcon className="h-5 w-5 text-gray-400 mx-auto" /></td>
                  <td className="py-4 px-6 text-center"><CheckIcon className="h-5 w-5 text-green-500 mx-auto" /></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="bg-white py-24">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-xl text-gray-600">
              Everything you need to know about our pricing and plans
            </p>
          </div>

          <div className="space-y-8">
            {faqs.map((faq) => (
              <div key={faq.question} className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  {faq.question}
                </h3>
                <p className="text-gray-600">
                  {faq.answer}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary-600 py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Get Started?
          </h2>
          <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
            Join thousands of companies already using our platform to win EU grants.
            Start your free trial today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/register" className="btn bg-white text-primary-600 hover:bg-primary-50 text-lg px-8 py-3">
              Start Free Trial
            </a>
            <a href="/contact" className="btn btn-outline border-white text-white hover:bg-white hover:text-primary-600 text-lg px-8 py-3">
              Contact Sales
            </a>
          </div>
        </div>
      </section>
    </div>
  )
}

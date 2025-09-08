import React from 'react'
import { MagnifyingGlassIcon, SparklesIcon, ChartBarIcon, DocumentTextIcon, RocketLaunchIcon, ShieldCheckIcon, ClockIcon, UserGroupIcon } from '@heroicons/react/24/outline'

export default function FeaturesPage() {
  const mainFeatures = [
    {
      icon: MagnifyingGlassIcon,
      title: 'Smart Grant Discovery',
      description: 'AI-powered search and filtering to find the most relevant EU funding opportunities for your business.',
      details: [
        'Advanced keyword matching and semantic search',
        'Industry-specific grant recommendations',
        'Real-time opportunity alerts',
        'Custom filtering by funding amount, deadline, and sector'
      ]
    },
    {
      icon: SparklesIcon,
      title: 'AI Application Assistant',
      description: 'Get personalized guidance and automated application drafting powered by advanced AI technology.',
      details: [
        'Automated application form pre-filling',
        'AI-generated proposal sections',
        'Compliance and eligibility checking',
        'Personalized improvement suggestions'
      ]
    },
    {
      icon: ChartBarIcon,
      title: 'Success Analytics',
      description: 'Track your application progress and get insights to improve your funding success rate.',
      details: [
        'Application success rate tracking',
        'Performance benchmarking',
        'Funding pipeline management',
        'ROI analysis and reporting'
      ]
    },
    {
      icon: DocumentTextIcon,
      title: 'Document Management',
      description: 'Organize and manage all your grant applications and supporting documents in one place.',
      details: [
        'Centralized document storage',
        'Version control and collaboration',
        'Template library and reuse',
        'Automated backup and sync'
      ]
    }
  ]

  const additionalFeatures = [
    {
      icon: RocketLaunchIcon,
      title: 'Fast Setup',
      description: 'Get started in minutes with our streamlined onboarding process'
    },
    {
      icon: ShieldCheckIcon,
      title: 'Secure & Compliant',
      description: 'Enterprise-grade security with GDPR compliance and data encryption'
    },
    {
      icon: ClockIcon,
      title: '24/7 Monitoring',
      description: 'Continuous monitoring for new opportunities and deadline alerts'
    },
    {
      icon: UserGroupIcon,
      title: 'Expert Support',
      description: 'Access to grant specialists and funding experts for guidance'
    }
  ]

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 text-white py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Powerful Features for
              <br />
              <span className="text-primary-200">Grant Success</span>
            </h1>
            <p className="text-xl md:text-2xl text-primary-100 mb-8 max-w-3xl mx-auto">
              Discover how our AI-powered platform streamlines every step of the EU grant application process,
              from discovery to submission and beyond.
            </p>
          </div>
        </div>
      </section>

      {/* Main Features Section */}
      <section className="bg-white py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Everything You Need to Win Grants
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our comprehensive suite of tools is designed to maximize your grant application success rate
            </p>
          </div>

          <div className="space-y-24">
            {mainFeatures.map((feature, index) => (
              <div key={feature.title} className={`flex flex-col lg:flex-row items-center gap-12 ${
                index % 2 === 1 ? 'lg:flex-row-reverse' : ''
              }`}>
                <div className="flex-1">
                  <div className="flex items-center mb-6">
                    <div className="h-12 w-12 bg-primary-100 rounded-lg flex items-center justify-center mr-4">
                      <feature.icon className="h-6 w-6 text-primary-600" />
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900">{feature.title}</h3>
                  </div>
                  <p className="text-lg text-gray-600 mb-6">{feature.description}</p>
                  <ul className="space-y-3">
                    {feature.details.map((detail) => (
                      <li key={detail} className="flex items-start">
                        <div className="h-2 w-2 bg-primary-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                        <span className="text-gray-700">{detail}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="flex-1">
                  <div className="bg-gradient-to-br from-gray-100 to-gray-200 rounded-xl h-80 flex items-center justify-center">
                    <feature.icon className="h-24 w-24 text-gray-400" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Additional Features Section */}
      <section className="bg-gray-50 py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Built for Performance
            </h2>
            <p className="text-xl text-gray-600">
              Additional features that make our platform the best choice for EU grant applications
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {additionalFeatures.map((feature) => (
              <div key={feature.title} className="card text-center">
                <div className="mx-auto h-12 w-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="h-6 w-6 text-primary-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-primary-600 mb-2">89%</div>
              <div className="text-gray-600">Success Rate Improvement</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary-600 mb-2">75%</div>
              <div className="text-gray-600">Time Saved on Applications</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary-600 mb-2">€2.4M</div>
              <div className="text-gray-600">Average Funding Won</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary-600 mb-2">48h</div>
              <div className="text-gray-600">Average Application Time</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary-600 py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Experience These Features?
          </h2>
          <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
            Start your free trial today and discover how our AI-powered platform can transform your grant success.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/register" className="btn bg-white text-primary-600 hover:bg-primary-50 text-lg px-8 py-3">
              Start Free Trial
            </a>
            <a href="/grants" className="btn btn-outline border-white text-white hover:bg-white hover:text-primary-600 text-lg px-8 py-3">
              Browse Grants
            </a>
          </div>
        </div>
      </section>
    </div>
  )
}

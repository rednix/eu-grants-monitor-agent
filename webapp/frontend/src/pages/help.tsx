import React from 'react'
import { MagnifyingGlassIcon, BookOpenIcon, ChatBubbleLeftRightIcon, EnvelopeIcon } from '@heroicons/react/24/outline'

export default function HelpPage() {
  const helpCategories = [
    {
      icon: BookOpenIcon,
      title: 'Getting Started',
      description: 'Learn the basics of using our platform',
      articles: [
        'Setting up your account',
        'Understanding the dashboard',
        'Your first grant search',
        'Creating saved searches'
      ]
    },
    {
      icon: MagnifyingGlassIcon,
      title: 'Grant Discovery',
      description: 'Find the perfect funding opportunities',
      articles: [
        'Advanced search filters',
        'Understanding grant categories',
        'Setting up alerts',
        'Reading grant requirements'
      ]
    },
    {
      icon: ChatBubbleLeftRightIcon,
      title: 'AI Assistant',
      description: 'Make the most of our AI-powered tools',
      articles: [
        'Using the application assistant',
        'Getting proposal suggestions',
        'Compliance checking',
        'Optimizing applications'
      ]
    },
    {
      icon: EnvelopeIcon,
      title: 'Account & Billing',
      description: 'Manage your subscription and settings',
      articles: [
        'Changing your plan',
        'Billing and payments',
        'Team management',
        'Account settings'
      ]
    }
  ]

  const popularArticles = [
    'How to search for grants effectively',
    'Understanding EU funding programs',
    'Tips for successful applications',
    'Using AI to improve your proposals',
    'Setting up email notifications',
    'Collaborative features for teams'
  ]

  const quickAnswers = [
    {
      question: 'How do I reset my password?',
      answer: 'Click "Forgot Password" on the login page and follow the email instructions.'
    },
    {
      question: 'Can I cancel my subscription anytime?',
      answer: 'Yes, you can cancel your subscription at any time from your account settings.'
    },
    {
      question: 'How accurate is the grant matching?',
      answer: 'Our AI achieves 95%+ accuracy by analyzing grant requirements against your profile.'
    },
    {
      question: 'Do you support multiple languages?',
      answer: 'Yes, we support all major EU languages for both interface and grant content.'
    }
  ]

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 text-white py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Help Center
            </h1>
            <p className="text-xl md:text-2xl text-primary-100 mb-8 max-w-3xl mx-auto">
              Find answers, guides, and resources to help you succeed with EU grant applications.
            </p>
            
            {/* Search Box */}
            <div className="max-w-2xl mx-auto">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search for help articles..."
                  className="w-full px-6 py-4 pl-12 text-gray-900 bg-white rounded-lg border-0 shadow-lg focus:ring-2 focus:ring-primary-300"
                />
                <MagnifyingGlassIcon className="absolute left-4 top-4 h-6 w-6 text-gray-400" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Help Categories */}
      <section className="bg-white py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Browse by Category
            </h2>
            <p className="text-xl text-gray-600">
              Find the information you need organized by topic
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {helpCategories.map((category) => (
              <div key={category.title} className="card">
                <div className="flex items-start space-x-4">
                  <div className="h-12 w-12 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <category.icon className="h-6 w-6 text-primary-600" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">{category.title}</h3>
                    <p className="text-gray-600 mb-4">{category.description}</p>
                    <ul className="space-y-2">
                      {category.articles.map((article) => (
                        <li key={article}>
                          <a href="#" className="text-primary-600 hover:text-primary-700 text-sm">
                            {article}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Popular Articles */}
      <section className="bg-gray-50 py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Popular Articles
            </h2>
            <p className="text-xl text-gray-600">
              Most frequently accessed help articles
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {popularArticles.map((article) => (
              <a
                key={article}
                href="#"
                className="card hover:shadow-lg transition-shadow"
              >
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{article}</h3>
                <p className="text-primary-600 text-sm">Read article →</p>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* Quick Answers */}
      <section className="bg-white py-24">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Quick Answers
            </h2>
            <p className="text-xl text-gray-600">
              Instant answers to common questions
            </p>
          </div>

          <div className="space-y-6">
            {quickAnswers.map((qa) => (
              <div key={qa.question} className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  {qa.question}
                </h3>
                <p className="text-gray-600">
                  {qa.answer}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Support */}
      <section className="bg-primary-600 py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Still Need Help?
          </h2>
          <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
            Can't find what you're looking for? Our support team is here to help.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/contact" className="btn bg-white text-primary-600 hover:bg-primary-50 text-lg px-8 py-3">
              Contact Support
            </a>
            <a href="mailto:support@eugrantsmonitor.com" className="btn btn-outline border-white text-white hover:bg-white hover:text-primary-600 text-lg px-8 py-3">
              Email Us
            </a>
          </div>
        </div>
      </section>
    </div>
  )
}

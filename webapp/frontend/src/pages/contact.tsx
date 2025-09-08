import React, { useState } from 'react'
import { EnvelopeIcon, PhoneIcon, MapPinIcon, ClockIcon } from '@heroicons/react/24/outline'

export default function ContactPage() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    company: '',
    subject: '',
    message: ''
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Handle form submission here
    console.log('Form submitted:', formData)
    // You would typically send this to your backend API
  }

  const contactInfo = [
    {
      icon: EnvelopeIcon,
      title: 'Email Us',
      content: 'support@eugrantsmonitor.com',
      description: 'Send us an email and we\'ll respond within 24 hours'
    },
    {
      icon: PhoneIcon,
      title: 'Call Us',
      content: '+32 2 123 4567',
      description: 'Mon-Fri from 9am to 6pm CET'
    },
    {
      icon: MapPinIcon,
      title: 'Visit Us',
      content: 'Brussels, Belgium',
      description: 'European Quarter, near EU institutions'
    },
    {
      icon: ClockIcon,
      title: 'Support Hours',
      content: '9:00 AM - 6:00 PM CET',
      description: 'Monday through Friday'
    }
  ]

  const subjects = [
    'General Inquiry',
    'Technical Support',
    'Sales Question',
    'Partnership Opportunity',
    'Billing Support',
    'Feature Request',
    'Bug Report',
    'Other'
  ]

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 text-white py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Get in Touch
            </h1>
            <p className="text-xl md:text-2xl text-primary-100 mb-8 max-w-3xl mx-auto">
              We're here to help you succeed with EU grant applications. 
              Reach out to our team of experts for support, sales, or partnership inquiries.
            </p>
          </div>
        </div>
      </section>

      {/* Contact Info Cards */}
      <section className="bg-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {contactInfo.map((info) => (
              <div key={info.title} className="card text-center">
                <div className="mx-auto h-12 w-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                  <info.icon className="h-6 w-6 text-primary-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{info.title}</h3>
                <p className="text-primary-600 font-medium mb-2">{info.content}</p>
                <p className="text-gray-600 text-sm">{info.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Form & Info */}
      <section className="bg-gray-50 py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Contact Form */}
            <div className="card">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Send us a Message</h2>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-2">
                      First Name *
                    </label>
                    <input
                      type="text"
                      id="firstName"
                      name="firstName"
                      required
                      value={formData.firstName}
                      onChange={handleChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                  <div>
                    <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-2">
                      Last Name *
                    </label>
                    <input
                      type="text"
                      id="lastName"
                      name="lastName"
                      required
                      value={formData.lastName}
                      onChange={handleChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    required
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>

                <div>
                  <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-2">
                    Company
                  </label>
                  <input
                    type="text"
                    id="company"
                    name="company"
                    value={formData.company}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>

                <div>
                  <label htmlFor="subject" className="block text-sm font-medium text-gray-700 mb-2">
                    Subject *
                  </label>
                  <select
                    id="subject"
                    name="subject"
                    required
                    value={formData.subject}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  >
                    <option value="">Select a subject...</option>
                    {subjects.map((subject) => (
                      <option key={subject} value={subject}>{subject}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
                    Message *
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    rows={6}
                    required
                    value={formData.message}
                    onChange={handleChange}
                    placeholder="Tell us how we can help you..."
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  ></textarea>
                </div>

                <button
                  type="submit"
                  className="btn btn-primary w-full"
                >
                  Send Message
                </button>
              </form>
            </div>

            {/* Contact Information */}
            <div className="space-y-8">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Let's Start a Conversation</h2>
                <p className="text-gray-600 mb-6">
                  Whether you're looking for more information about our platform, need technical support, 
                  or want to explore partnership opportunities, we're here to help.
                </p>
                <p className="text-gray-600">
                  Our team of EU funding experts is ready to assist you with any questions about grant 
                  applications, platform features, or finding the right funding opportunities for your business.
                </p>
              </div>

              {/* Quick Links */}
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
                <div className="space-y-3">
                  <a href="/help" className="block text-primary-600 hover:text-primary-700 font-medium">
                    → Visit our Help Center
                  </a>
                  <a href="/api-docs" className="block text-primary-600 hover:text-primary-700 font-medium">
                    → View API Documentation
                  </a>
                  <a href="/pricing" className="block text-primary-600 hover:text-primary-700 font-medium">
                    → See Pricing Plans
                  </a>
                  <a href="/grants" className="block text-primary-600 hover:text-primary-700 font-medium">
                    → Browse Grant Opportunities
                  </a>
                </div>
              </div>

              {/* Response Times */}
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Response Times</h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-700">General Inquiries</span>
                    <span className="text-primary-600 font-medium">Within 24 hours</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-700">Technical Support</span>
                    <span className="text-primary-600 font-medium">Within 4 hours</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-700">Sales Questions</span>
                    <span className="text-primary-600 font-medium">Within 2 hours</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-700">Urgent Issues</span>
                    <span className="text-primary-600 font-medium">Within 1 hour</span>
                  </div>
                </div>
              </div>

              {/* Office Info */}
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Our Office</h3>
                <div className="space-y-2 text-gray-600">
                  <p>EU Grants Monitor</p>
                  <p>European Quarter</p>
                  <p>1000 Brussels, Belgium</p>
                  <p className="mt-4 text-sm">
                    Located in the heart of Brussels, close to the European Commission and Parliament.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="bg-white py-24">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Common Questions
            </h2>
            <p className="text-xl text-gray-600">
              Find quick answers to frequently asked questions
            </p>
          </div>

          <div className="space-y-8">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                How quickly can you respond to support requests?
              </h3>
              <p className="text-gray-600">
                We aim to respond to all support requests within 4 hours during business hours. 
                Urgent issues are typically addressed within 1 hour.
              </p>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Do you offer phone support?
              </h3>
              <p className="text-gray-600">
                Yes, phone support is available for Professional and Enterprise plan customers. 
                We also offer scheduled calls for complex technical discussions.
              </p>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Can you help with grant application strategy?
              </h3>
              <p className="text-gray-600">
                Absolutely! Our team includes EU funding experts who can provide strategic guidance, 
                application reviews, and best practice recommendations.
              </p>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                What languages do you support?
              </h3>
              <p className="text-gray-600">
                Our platform supports multiple EU languages, and our support team can assist in 
                English, French, German, Spanish, and Italian.
              </p>
            </div>
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
            Don't wait - start discovering EU funding opportunities today with our free trial.
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

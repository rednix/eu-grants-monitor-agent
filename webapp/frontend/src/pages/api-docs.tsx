import React from 'react'
import { CodeBracketIcon, BookOpenIcon, KeyIcon, GlobeAltIcon } from '@heroicons/react/24/outline'

export default function ApiDocsPage() {
  const endpoints = [
    {
      method: 'GET',
      path: '/api/v1/grants',
      description: 'Retrieve paginated list of grants with optional filters',
      auth: true
    },
    {
      method: 'GET',
      path: '/api/v1/grants/{id}',
      description: 'Get detailed information about a specific grant',
      auth: true
    },
    {
      method: 'POST',
      path: '/api/v1/grants/search',
      description: 'Perform advanced search with multiple criteria',
      auth: true
    },
    {
      method: 'GET',
      path: '/api/v1/applications',
      description: 'List user\'s grant applications',
      auth: true
    },
    {
      method: 'POST',
      path: '/api/v1/applications',
      description: 'Submit a new grant application',
      auth: true
    }
  ]

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 text-white py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              API Documentation
            </h1>
            <p className="text-xl md:text-2xl text-primary-100 mb-8 max-w-3xl mx-auto">
              Integrate EU grant data into your applications with our comprehensive REST API.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a href="#getting-started" className="btn bg-white text-primary-600 hover:bg-primary-50 text-lg px-8 py-3">
                Get Started
              </a>
              <a href="#endpoints" className="btn btn-outline border-white text-white hover:bg-white hover:text-primary-600 text-lg px-8 py-3">
                View Endpoints
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Quick Info Cards */}
      <section className="bg-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="card text-center">
              <div className="mx-auto h-12 w-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <GlobeAltIcon className="h-6 w-6 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">REST API</h3>
              <p className="text-gray-600 text-sm">JSON-based REST API with standard HTTP methods</p>
            </div>
            
            <div className="card text-center">
              <div className="mx-auto h-12 w-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <KeyIcon className="h-6 w-6 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">API Keys</h3>
              <p className="text-gray-600 text-sm">Secure authentication with API key headers</p>
            </div>
            
            <div className="card text-center">
              <div className="mx-auto h-12 w-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <CodeBracketIcon className="h-6 w-6 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Rate Limited</h3>
              <p className="text-gray-600 text-sm">Fair usage with 1000 requests per hour</p>
            </div>
            
            <div className="card text-center">
              <div className="mx-auto h-12 w-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <BookOpenIcon className="h-6 w-6 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">OpenAPI</h3>
              <p className="text-gray-600 text-sm">Complete OpenAPI 3.0 specification available</p>
            </div>
          </div>
        </div>
      </section>

      {/* Getting Started */}
      <section id="getting-started" className="bg-gray-50 py-24">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Getting Started
            </h2>
            <p className="text-xl text-gray-600">
              Quick setup guide to start using the API
            </p>
          </div>

          <div className="space-y-8">
            <div className="card">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">1. Get Your API Key</h3>
              <p className="text-gray-600 mb-4">
                Generate your API key from your account dashboard. Enterprise customers can create multiple keys for different applications.
              </p>
              <div className="bg-gray-100 p-4 rounded-lg">
                <code className="text-sm">
                  Dashboard → Settings → API Keys → Generate New Key
                </code>
              </div>
            </div>

            <div className="card">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">2. Authentication</h3>
              <p className="text-gray-600 mb-4">
                Include your API key in the Authorization header of all requests:
              </p>
              <div className="bg-gray-100 p-4 rounded-lg">
                <code className="text-sm">
                  Authorization: Bearer YOUR_API_KEY
                </code>
              </div>
            </div>

            <div className="card">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">3. Make Your First Request</h3>
              <p className="text-gray-600 mb-4">
                Try fetching the latest grants:
              </p>
              <div className="bg-gray-100 p-4 rounded-lg">
                <pre className="text-sm">
{`curl -X GET "https://api.eugrantsmonitor.com/v1/grants" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json"`}
                </pre>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* API Endpoints */}
      <section id="endpoints" className="bg-white py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              API Endpoints
            </h2>
            <p className="text-xl text-gray-600">
              Complete list of available endpoints
            </p>
          </div>

          <div className="space-y-4">
            {endpoints.map((endpoint, index) => (
              <div key={index} className="card">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <span className={`inline-block px-3 py-1 text-xs font-medium rounded-full ${
                        endpoint.method === 'GET' ? 'bg-blue-100 text-blue-800' :
                        endpoint.method === 'POST' ? 'bg-green-100 text-green-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {endpoint.method}
                      </span>
                      <code className="text-lg font-mono text-gray-900">
                        {endpoint.path}
                      </code>
                    </div>
                    <p className="text-gray-600 mb-2">{endpoint.description}</p>
                  </div>
                  {endpoint.auth && (
                    <div className="ml-4">
                      <span className="inline-block bg-yellow-100 text-yellow-800 text-xs font-medium px-2 py-1 rounded-full">
                        Auth Required
                      </span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Example Response */}
      <section className="bg-gray-50 py-24">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Example Response
            </h2>
            <p className="text-xl text-gray-600">
              Sample response from the grants endpoint
            </p>
          </div>

          <div className="card">
            <div className="bg-gray-900 rounded-lg p-6 overflow-auto">
              <pre className="text-green-400 text-sm">
{`{
  "data": [
    {
      "id": "HE-2024-001",
      "title": "Horizon Europe Digital Innovation",
      "program": "Horizon Europe",
      "synopsis": "Support for digital transformation...",
      "funding_amount": {
        "min": 500000,
        "max": 2000000,
        "currency": "EUR"
      },
      "deadline": "2024-03-15T23:59:59Z",
      "status": "open",
      "technology_areas": ["AI", "IoT", "Blockchain"],
      "eligibility": {
        "organization_types": ["SME", "Research"],
        "countries": ["EU27", "Associated"]
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 1247,
    "has_next": true
  }
}`}
              </pre>
            </div>
          </div>
        </div>
      </section>

      {/* Support */}
      <section className="bg-primary-600 py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Need API Support?
          </h2>
          <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
            Our developer support team is ready to help you integrate our API.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/contact" className="btn bg-white text-primary-600 hover:bg-primary-50 text-lg px-8 py-3">
              Contact Support
            </a>
            <a href="mailto:api-support@eugrantsmonitor.com" className="btn btn-outline border-white text-white hover:bg-white hover:text-primary-600 text-lg px-8 py-3">
              Email API Team
            </a>
          </div>
        </div>
      </section>
    </div>
  )
}

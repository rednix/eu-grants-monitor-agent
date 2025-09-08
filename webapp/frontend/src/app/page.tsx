import Link from 'next/link'
import { ArrowRight, Search, Target, Brain, Shield } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">EU Grants Monitor</h1>
            </div>
            <div className="flex space-x-4">
              <Link 
                href="/login"
                className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                Sign in
              </Link>
              <Link 
                href="/signup"
                className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
              Discover EU Funding
              <span className="text-indigo-600"> Opportunities</span>
            </h1>
            <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
              AI-powered platform that helps your company find, analyze, and apply for EU grants. 
              Join thousands of successful applicants.
            </p>
            <div className="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
              <div className="rounded-md shadow">
                <Link 
                  href="/signup"
                  className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10"
                >
                  Start Free Trial
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </div>
              <div className="mt-3 rounded-md shadow sm:mt-0 sm:ml-3">
                <Link 
                  href="/login"
                  className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10"
                >
                  Sign In
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h2 className="text-base text-indigo-600 font-semibold tracking-wide uppercase">Features</h2>
              <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
                Everything you need to secure EU funding
              </p>
            </div>

            <div className="mt-10">
              <div className="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-4">
                {/* Feature 1 */}
                <div className="text-center">
                  <div className="mx-auto h-12 w-12 bg-indigo-100 rounded-md flex items-center justify-center">
                    <Search className="h-6 w-6 text-indigo-600" />
                  </div>
                  <h3 className="mt-6 text-lg leading-6 font-medium text-gray-900">Smart Discovery</h3>
                  <p className="mt-2 text-base text-gray-500">
                    AI-powered search finds grants perfectly matched to your company's profile and expertise.
                  </p>
                </div>

                {/* Feature 2 */}
                <div className="text-center">
                  <div className="mx-auto h-12 w-12 bg-indigo-100 rounded-md flex items-center justify-center">
                    <Target className="h-6 w-6 text-indigo-600" />
                  </div>
                  <h3 className="mt-6 text-lg leading-6 font-medium text-gray-900">Precision Matching</h3>
                  <p className="mt-2 text-base text-gray-500">
                    Advanced filtering by industry, company size, funding amount, and project duration.
                  </p>
                </div>

                {/* Feature 3 */}
                <div className="text-center">
                  <div className="mx-auto h-12 w-12 bg-indigo-100 rounded-md flex items-center justify-center">
                    <Brain className="h-6 w-6 text-indigo-600" />
                  </div>
                  <h3 className="mt-6 text-lg leading-6 font-medium text-gray-900">AI Assistant</h3>
                  <p className="mt-2 text-base text-gray-500">
                    Get personalized guidance and automated application assistance powered by AI.
                  </p>
                </div>

                {/* Feature 4 */}
                <div className="text-center">
                  <div className="mx-auto h-12 w-12 bg-indigo-100 rounded-md flex items-center justify-center">
                    <Shield className="h-6 w-6 text-indigo-600" />
                  </div>
                  <h3 className="mt-6 text-lg leading-6 font-medium text-gray-900">Secure & Reliable</h3>
                  <p className="mt-2 text-base text-gray-500">
                    Enterprise-grade security with real-time updates from official EU grant databases.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="bg-indigo-50">
          <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8 lg:flex lg:items-center lg:justify-between">
            <h2 className="text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              <span className="block">Ready to get started?</span>
              <span className="block text-indigo-600">Create your account today.</span>
            </h2>
            <div className="mt-8 flex lg:mt-0 lg:flex-shrink-0">
              <div className="inline-flex rounded-md shadow">
                <Link 
                  href="/signup"
                  className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                >
                  Get Started Free
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white">
        <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 md:px-8">
          <div className="text-center text-gray-500">
            <p>&copy; 2024 EU Grants Monitor. All rights reserved.</p>
            <p className="mt-2 text-sm">
              Helping European companies access funding opportunities since 2024.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

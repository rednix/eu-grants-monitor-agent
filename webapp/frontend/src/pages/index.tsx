import { useState, useEffect } from 'react'
import Link from 'next/link'
import { MagnifyingGlassIcon, SparklesIcon, ChartBarIcon, DocumentTextIcon } from '@heroicons/react/24/outline'
import { grantsApi } from '@/utils/api'
import { Grant } from '@/types'

export default function HomePage() {
  const [featuredGrants, setFeaturedGrants] = useState<Grant[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadFeaturedGrants = async () => {
      try {
        const response = await grantsApi.getGrants({}, 1, 6)
        setFeaturedGrants(response.data)
      } catch (error) {
        console.error('Failed to load featured grants:', error)
      } finally {
        setLoading(false)
      }
    }

    loadFeaturedGrants()
  }, [])

  const features = [
    {
      icon: MagnifyingGlassIcon,
      title: 'Smart Grant Discovery',
      description: 'AI-powered search and filtering to find the most relevant EU funding opportunities for your business.'
    },
    {
      icon: SparklesIcon,
      title: 'AI Application Assistant',
      description: 'Get personalized guidance and automated application drafting powered by advanced AI technology.'
    },
    {
      icon: ChartBarIcon,
      title: 'Success Analytics',
      description: 'Track your application progress and get insights to improve your funding success rate.'
    },
    {
      icon: DocumentTextIcon,
      title: 'Document Management',
      description: 'Organize and manage all your grant applications and supporting documents in one place.'
    }
  ]

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 text-white">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Discover EU Funding
              <br />
              <span className="text-primary-200">Made Simple</span>
            </h1>
            <p className="text-xl md:text-2xl text-primary-100 mb-8 max-w-3xl mx-auto">
              AI-powered platform helping SMEs find, apply for, and win EU grants. 
              From Horizon Europe to Digital Europe - we've got you covered.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/grants" className="btn bg-white text-primary-600 hover:bg-primary-50 text-lg px-8 py-3">
                Browse Grants
              </Link>
              <Link href="/register" className="btn btn-outline border-white text-white hover:bg-white hover:text-primary-600 text-lg px-8 py-3">
                Get Started Free
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-primary-600 mb-2">€95.5B</div>
              <div className="text-gray-600">Available EU Funding</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary-600 mb-2">1,500+</div>
              <div className="text-gray-600">Active Opportunities</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary-600 mb-2">89%</div>
              <div className="text-gray-600">Success Rate Improvement</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary-600 mb-2">2,400+</div>
              <div className="text-gray-600">SMEs Funded</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-gray-50 py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Everything You Need to Win Grants
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              From discovery to submission, our AI-powered platform streamlines every step of the grant application process.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature) => (
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

      {/* Featured Grants Section */}
      <section className="bg-white py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Featured Grant Opportunities
            </h2>
            <p className="text-xl text-gray-600">
              Discover the latest EU funding opportunities perfect for your business
            </p>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <div key={i} className="card animate-pulse">
                  <div className="h-4 bg-gray-200 rounded mb-4"></div>
                  <div className="h-6 bg-gray-200 rounded mb-3"></div>
                  <div className="h-20 bg-gray-200 rounded mb-4"></div>
                  <div className="h-4 bg-gray-200 rounded mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {featuredGrants.map((grant) => (
                <div key={grant.id} className="card hover:shadow-lg transition-shadow">
                  <div className="mb-4">
                    <span className="inline-block bg-primary-100 text-primary-800 text-xs px-2 py-1 rounded-full font-medium">
                      {grant.program}
                    </span>
                    <div className="flex justify-between items-start mt-2">
                      <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
                        {grant.title}
                      </h3>
                    </div>
                  </div>
                  
                  <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                    {grant.synopsis || grant.description}
                  </p>
                  
                  <div className="flex justify-between items-center text-sm text-gray-500 mb-4">
                    <div>
                      €{grant.min_funding_amount?.toLocaleString()} - €{grant.max_funding_amount?.toLocaleString()}
                    </div>
                    <div>
                      Deadline: {new Date(grant.deadline).toLocaleDateString()}
                    </div>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <div className="flex flex-wrap gap-1">
                      {grant.technology_areas?.slice(0, 2).map((area) => (
                        <span key={area} className="bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded">
                          {area}
                        </span>
                      ))}
                    </div>
                    <Link href={`/grants/${grant.grant_id}`} className="btn btn-outline btn-sm">
                      View Details
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="text-center mt-12">
            <Link href="/grants" className="btn btn-primary btn-lg">
              View All Grants
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary-600 py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Transform Your Grant Success?
          </h2>
          <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
            Join thousands of SMEs already using our platform to discover and win EU funding opportunities.
          </p>
          <Link href="/register" className="btn bg-white text-primary-600 hover:bg-primary-50 text-lg px-8 py-3">
            Start Your Free Trial
          </Link>
        </div>
      </section>
    </div>
  )
}

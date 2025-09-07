import { useState, useEffect } from 'react'
import Link from 'next/link'
import { MagnifyingGlassIcon, FunnelIcon, CalendarIcon, CurrencyEuroIcon } from '@heroicons/react/24/outline'
import { grantsApi } from '@/utils/api'
import { Grant, GrantFilters } from '@/types'

export default function GrantsPage() {
  const [grants, setGrants] = useState<Grant[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filters, setFilters] = useState<GrantFilters>({})
  const [showFilters, setShowFilters] = useState(false)
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    per_page: 20,
    total_pages: 0
  })

  const programs = ['Horizon Europe', 'Digital Europe', 'Life', 'Erasmus+', 'Creative Europe']
  const techAreas = ['AI', 'Healthcare', 'Manufacturing', 'Environmental', 'IoT', 'Blockchain', 'Robotics']
  const countries = ['DE', 'FR', 'IT', 'ES', 'NL', 'BE', 'AT', 'SE', 'DK', 'FI', 'PT', 'GR']

  useEffect(() => {
    loadGrants()
  }, [filters, pagination.page])

  const loadGrants = async () => {
    setLoading(true)
    try {
      const searchFilters = { ...filters }
      if (searchTerm) {
        searchFilters.search = searchTerm
      }
      
      const response = await grantsApi.getGrants(searchFilters, pagination.page, pagination.per_page)
      setGrants(response.data)
      setPagination({
        ...pagination,
        total: response.total,
        total_pages: response.total_pages
      })
    } catch (error) {
      console.error('Failed to load grants:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    setPagination(prev => ({ ...prev, page: 1 }))
    loadGrants()
  }

  const handleFilterChange = (key: keyof GrantFilters, value: any) => {
    setFilters(prev => ({ ...prev, [key]: value }))
    setPagination(prev => ({ ...prev, page: 1 }))
  }

  const clearFilters = () => {
    setFilters({})
    setSearchTerm('')
    setPagination(prev => ({ ...prev, page: 1 }))
  }

  return (
    <div className="bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              EU Grant Opportunities
            </h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Discover funding opportunities from across the European Union. Use our advanced search and AI-powered matching to find the perfect grants for your business.
            </p>
          </div>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar Filters */}
          <div className="lg:w-1/4">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 sticky top-4">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-gray-900">Filters</h2>
                <button
                  onClick={clearFilters}
                  className="text-sm text-primary-600 hover:text-primary-700"
                >
                  Clear all
                </button>
              </div>

              {/* Search */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Search
                </label>
                <form onSubmit={handleSearch}>
                  <div className="relative">
                    <input
                      type="text"
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="input pr-10"
                      placeholder="Search grants..."
                    />
                    <button
                      type="submit"
                      className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    >
                      <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
                    </button>
                  </div>
                </form>
              </div>

              {/* Program Filter */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Program
                </label>
                <select
                  value={filters.program || ''}
                  onChange={(e) => handleFilterChange('program', e.target.value || undefined)}
                  className="input"
                >
                  <option value="">All Programs</option>
                  {programs.map((program) => (
                    <option key={program} value={program}>{program}</option>
                  ))}
                </select>
              </div>

              {/* Funding Amount */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Funding Amount (€)
                </label>
                <div className="grid grid-cols-2 gap-2">
                  <input
                    type="number"
                    placeholder="Min"
                    value={filters.min_amount || ''}
                    onChange={(e) => handleFilterChange('min_amount', e.target.value ? parseInt(e.target.value) : undefined)}
                    className="input"
                  />
                  <input
                    type="number"
                    placeholder="Max"
                    value={filters.max_amount || ''}
                    onChange={(e) => handleFilterChange('max_amount', e.target.value ? parseInt(e.target.value) : undefined)}
                    className="input"
                  />
                </div>
              </div>

              {/* Technology Areas */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Technology Areas
                </label>
                <div className="space-y-2 max-h-40 overflow-y-auto">
                  {techAreas.map((area) => (
                    <label key={area} className="flex items-center">
                      <input
                        type="checkbox"
                        checked={(filters.technology_areas || []).includes(area)}
                        onChange={(e) => {
                          const current = filters.technology_areas || []
                          if (e.target.checked) {
                            handleFilterChange('technology_areas', [...current, area])
                          } else {
                            handleFilterChange('technology_areas', current.filter(a => a !== area))
                          }
                        }}
                        className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                      />
                      <span className="ml-2 text-sm text-gray-700">{area}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:w-3/4">
            {/* Results Header */}
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-4">
                <h2 className="text-lg font-semibold text-gray-900">
                  {loading ? 'Loading...' : `${pagination.total} grants found`}
                </h2>
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className="lg:hidden btn btn-secondary"
                >
                  <FunnelIcon className="h-5 w-5 mr-2" />
                  Filters
                </button>
              </div>
            </div>

            {/* Grant Cards */}
            {loading ? (
              <div className="grid grid-cols-1 gap-6">
                {[1, 2, 3, 4, 5].map((i) => (
                  <div key={i} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
                    <div className="h-4 bg-gray-200 rounded mb-4 w-1/4"></div>
                    <div className="h-6 bg-gray-200 rounded mb-3 w-3/4"></div>
                    <div className="h-16 bg-gray-200 rounded mb-4"></div>
                    <div className="h-4 bg-gray-200 rounded mb-2 w-1/2"></div>
                  </div>
                ))}
              </div>
            ) : grants.length === 0 ? (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
                <MagnifyingGlassIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">No grants found</h3>
                <p className="text-gray-600 mb-4">
                  Try adjusting your search terms or filters to find more opportunities.
                </p>
                <button onClick={clearFilters} className="btn btn-primary">
                  Clear Filters
                </button>
              </div>
            ) : (
              <div className="space-y-6">
                {grants.map((grant) => (
                  <div key={grant.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
                    <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between mb-4">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <span className="inline-block bg-primary-100 text-primary-800 text-xs px-2 py-1 rounded-full font-medium">
                            {grant.program}
                          </span>
                          <span className={`inline-block text-xs px-2 py-1 rounded-full font-medium ${
                            grant.status === 'open' 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-gray-100 text-gray-800'
                          }`}>
                            {grant.status}
                          </span>
                        </div>
                        
                        <h3 className="text-xl font-semibold text-gray-900 mb-2">
                          <Link href={`/grants/${grant.grant_id}`} className="hover:text-primary-600">
                            {grant.title}
                          </Link>
                        </h3>
                        
                        <p className="text-gray-600 mb-4 line-clamp-3">
                          {grant.synopsis || grant.description}
                        </p>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                      <div className="flex items-center text-sm text-gray-500">
                        <CurrencyEuroIcon className="h-5 w-5 mr-2" />
                        €{grant.min_funding_amount?.toLocaleString()} - €{grant.max_funding_amount?.toLocaleString()}
                      </div>
                      <div className="flex items-center text-sm text-gray-500">
                        <CalendarIcon className="h-5 w-5 mr-2" />
                        Deadline: {new Date(grant.deadline).toLocaleDateString()}
                      </div>
                      <div className="text-sm text-gray-500">
                        Duration: {grant.project_duration_months} months
                      </div>
                    </div>

                    <div className="flex flex-wrap items-center justify-between">
                      <div className="flex flex-wrap gap-1 mb-2 lg:mb-0">
                        {grant.technology_areas?.slice(0, 3).map((area) => (
                          <span key={area} className="bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded">
                            {area}
                          </span>
                        ))}
                        {grant.technology_areas && grant.technology_areas.length > 3 && (
                          <span className="text-gray-500 text-xs">+{grant.technology_areas.length - 3} more</span>
                        )}
                      </div>
                      
                      <div className="flex items-center space-x-3">
                        <div className="text-sm text-gray-500">
                          Complexity: {Math.round(grant.complexity_score)}/100
                        </div>
                        <Link href={`/grants/${grant.grant_id}`} className="btn btn-primary btn-sm">
                          View Details
                        </Link>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Pagination */}
            {!loading && grants.length > 0 && pagination.total_pages > 1 && (
              <div className="flex items-center justify-center space-x-2 mt-8">
                <button
                  onClick={() => setPagination(prev => ({ ...prev, page: Math.max(1, prev.page - 1) }))}
                  disabled={pagination.page === 1}
                  className="btn btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
                
                <div className="flex items-center space-x-2">
                  {Array.from({ length: Math.min(5, pagination.total_pages) }, (_, i) => {
                    const page = i + 1
                    return (
                      <button
                        key={page}
                        onClick={() => setPagination(prev => ({ ...prev, page }))}
                        className={`w-10 h-10 rounded-lg text-sm font-medium transition-colors ${
                          pagination.page === page
                            ? 'bg-primary-600 text-white'
                            : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                        }`}
                      >
                        {page}
                      </button>
                    )
                  })}
                </div>
                
                <button
                  onClick={() => setPagination(prev => ({ ...prev, page: Math.min(prev.total_pages, prev.page + 1) }))}
                  disabled={pagination.page === pagination.total_pages}
                  className="btn btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

import Link from 'next/link'
import { authApi } from '@/utils/api'
import { CheckIcon } from '@heroicons/react/24/outline'

export default function RegisterPage() {
  const handleGoogleLogin = () => {
    authApi.loginWithGoogle()
  }

  const handleMicrosoftLogin = () => {
    authApi.loginWithMicrosoft()
  }

  const features = [
    'Access to 1,500+ EU grant opportunities',
    'AI-powered grant matching for your business',
    'Real-time updates on new funding opportunities',
    'Advanced search and filtering tools',
    'Application deadline tracking',
    'Company profile and preferences management'
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="flex">
        {/* Left side - Form */}
        <div className="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
          <div className="mx-auto w-full max-w-sm lg:w-96">
            <div>
              <div className="flex items-center">
                <div className="h-10 w-10 bg-primary-600 rounded-lg flex items-center justify-center mr-3">
                  <span className="text-white font-bold">EU</span>
                </div>
                <span className="text-2xl font-bold text-gray-900">Grants Monitor</span>
              </div>
              <h2 className="mt-6 text-3xl font-bold tracking-tight text-gray-900">
                Get Started for Free
              </h2>
              <p className="mt-2 text-sm text-gray-600">
                Join thousands of SMEs discovering EU funding opportunities
              </p>
            </div>

            <div className="mt-8">
              <div className="space-y-4">
                {/* Google OAuth Button */}
                <button
                  onClick={handleGoogleLogin}
                  className="w-full flex justify-center items-center px-4 py-3 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors"
                >
                  <svg className="w-5 h-5 mr-3" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                  </svg>
                  Continue with Google
                </button>

                {/* Microsoft OAuth Button */}
                <button
                  onClick={handleMicrosoftLogin}
                  className="w-full flex justify-center items-center px-4 py-3 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors"
                >
                  <svg className="w-5 h-5 mr-3" viewBox="0 0 24 24">
                    <path fill="#F35325" d="M1 1h10v10H1z"/>
                    <path fill="#81BC06" d="M13 1h10v10H13z"/>
                    <path fill="#05A6F0" d="M1 13h10v10H1z"/>
                    <path fill="#FFBA08" d="M13 13h10v10H13z"/>
                  </svg>
                  Continue with Microsoft
                </button>
              </div>

              <div className="mt-6 text-center text-sm text-gray-500">
                Already have an account?{' '}
                <Link href="/login" className="font-medium text-primary-600 hover:text-primary-500">
                  Sign in here
                </Link>
              </div>

              <div className="mt-8 text-center text-xs text-gray-500">
                By creating an account, you agree to our{' '}
                <Link href="/terms" className="text-primary-600 hover:text-primary-500">
                  Terms of Service
                </Link>{' '}
                and{' '}
                <Link href="/privacy" className="text-primary-600 hover:text-primary-500">
                  Privacy Policy
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Right side - Features */}
        <div className="hidden lg:block relative w-0 flex-1">
          <div className="absolute inset-0 bg-gradient-to-br from-primary-600 to-primary-900">
            <div className="h-full flex flex-col justify-center px-12">
              <div className="text-white">
                <h3 className="text-2xl font-bold mb-8">
                  Everything you need to win EU grants
                </h3>
                
                <div className="space-y-4">
                  {features.map((feature, index) => (
                    <div key={index} className="flex items-center">
                      <div className="flex-shrink-0">
                        <CheckIcon className="h-6 w-6 text-primary-200" />
                      </div>
                      <div className="ml-3 text-primary-100">{feature}</div>
                    </div>
                  ))}
                </div>

                <div className="mt-12 p-6 bg-white/10 rounded-lg backdrop-blur">
                  <div className="text-primary-100 text-sm mb-2">🚀 Free Plan Includes:</div>
                  <div className="text-white font-semibold">
                    • Browse all grants<br/>
                    • Basic search filters<br/>
                    • Deadline notifications<br/>
                    • Company profile setup
                  </div>
                  <div className="mt-3 text-primary-200 text-xs">
                    Upgrade anytime for AI-powered application assistance
                  </div>
                </div>

                <div className="mt-8 text-primary-200 text-sm">
                  "This platform helped us secure €250,000 in EU funding for our AI healthcare project. The grant matching is incredibly accurate!" 
                  <div className="mt-2 font-medium">— Maria Santos, CEO TechMed Solutions</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

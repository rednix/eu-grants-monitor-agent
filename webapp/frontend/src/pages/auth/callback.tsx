import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'

export default function AuthCallback() {
  const router = useRouter()
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading')
  const [message, setMessage] = useState('')

  useEffect(() => {
    const handleAuthCallback = async () => {
      const { token, error } = router.query

      if (error) {
        setStatus('error')
        setMessage(`Authentication failed: ${error}`)
        setTimeout(() => {
          router.push('/login')
        }, 3000)
        return
      }

      if (token && typeof token === 'string') {
        try {
          // Store the token
          localStorage.setItem('auth_token', token)
          
          // Verify the token by trying to get user info
          const response = await fetch('/api/auth/me', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          })

          if (response.ok) {
            setStatus('success')
            setMessage('Authentication successful! Redirecting...')
            
            // Redirect to dashboard or home page
            setTimeout(() => {
              router.push('/dashboard')
            }, 1500)
          } else {
            throw new Error('Invalid token')
          }
        } catch (err) {
          setStatus('error')
          setMessage('Authentication failed. Please try again.')
          localStorage.removeItem('auth_token')
          setTimeout(() => {
            router.push('/login')
          }, 3000)
        }
      } else {
        setStatus('error')
        setMessage('No authentication token received.')
        setTimeout(() => {
          router.push('/login')
        }, 3000)
      }
    }

    if (router.isReady) {
      handleAuthCallback()
    }
  }, [router])

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <div className="h-12 w-12 bg-primary-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold">EU</span>
          </div>
        </div>
        
        <div className="mt-8 bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <div className="text-center">
            {status === 'loading' && (
              <>
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
                <h2 className="mt-4 text-lg font-medium text-gray-900">
                  Completing authentication...
                </h2>
                <p className="mt-2 text-sm text-gray-500">
                  Please wait while we sign you in.
                </p>
              </>
            )}
            
            {status === 'success' && (
              <>
                <div className="mx-auto flex items-center justify-center h-8 w-8 rounded-full bg-green-100">
                  <svg className="h-5 w-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                </div>
                <h2 className="mt-4 text-lg font-medium text-green-900">
                  Authentication Successful
                </h2>
                <p className="mt-2 text-sm text-green-700">{message}</p>
              </>
            )}
            
            {status === 'error' && (
              <>
                <div className="mx-auto flex items-center justify-center h-8 w-8 rounded-full bg-red-100">
                  <svg className="h-5 w-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </div>
                <h2 className="mt-4 text-lg font-medium text-red-900">
                  Authentication Failed
                </h2>
                <p className="mt-2 text-sm text-red-700">{message}</p>
                <p className="mt-4 text-xs text-gray-500">
                  Redirecting to login page...
                </p>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

import { ReactNode } from 'react'
import Head from 'next/head'
import Header from './layout/Header'
import Footer from './layout/Footer'

interface LayoutProps {
  children: ReactNode
  title?: string
}

export default function Layout({ children, title = 'EU Grants Monitor' }: LayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>{title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      
      <Header />
      
      <main className="flex-1">
        {children}
      </main>
      
      <Footer />
    </div>
  )
}

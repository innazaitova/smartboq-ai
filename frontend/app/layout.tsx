// Next.js App Router Layout
'use client'

import './globals.css'
import { Inter } from 'next/font/google'
import { Toaster } from 'react-hot-toast'
import { useEffect } from 'react'
import { useAuthStore } from '../lib/store'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const { checkAuth } = useAuthStore()

  useEffect(() => {
    // Initialize auth state from localStorage on app load
    checkAuth()
  }, [])

  return (
    <html lang="en">
      <head>
        <title>QuantiBot AI - AI-Powered Quantity Surveying</title>
        <meta name="description" content="Transform 20 hours of manual QS work into 30 minutes with AI" />
        <meta name="keywords" content="quantity surveying, construction, BOQ, cost estimation, AI" />
      </head>
      <body className={inter.className}>
        {children}
        <Toaster position="top-right" />
      </body>
    </html>
  )
}

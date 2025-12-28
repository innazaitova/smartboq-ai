// Next.js App Router Layout
import './globals.css'
import { Inter } from 'next/font/google'
import { Toaster } from 'react-hot-toast'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'QuantiBot AI - AI-Powered Quantity Surveying',
  description: 'Transform 20 hours of manual QS work into 30 minutes with AI',
  keywords: 'quantity surveying, construction, BOQ, cost estimation, AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
        <Toaster position="top-right" />
      </body>
    </html>
  )
}

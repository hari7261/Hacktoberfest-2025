import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const timer = setTimeout(() => {
      router.push('/social-media');
    }, 2000);
    return () => clearTimeout(timer);
  }, [router]);

  return (
    <>
      <Head>
        <title>Social Media Analytics Dashboard</title>
        <meta name="description" content="Track and analyze your social media performance" />
      </Head>
      <div className="min-h-screen bg-gradient-to-br from-pink-500 via-purple-700 to-indigo-900 flex items-center justify-center">
        <div className="text-center">
          <p className="text-white text-2xl font-bold mb-6 animate-fade-in">Redirecting to Social Media Dashboard...</p>
          <div className="flex justify-center items-center space-x-2">
            <span className="loader-dot bg-pink-400 animate-bounce"></span>
            <span className="loader-dot bg-purple-400 animate-bounce delay-150"></span>
            <span className="loader-dot bg-indigo-400 animate-bounce delay-300"></span>
          </div>
        </div>
      </div>
      <style jsx global>{`
        .loader-dot {
          width: 16px;
          height: 16px;
          border-radius: 50%;
          display: inline-block;
        }
        .animate-fade-in {
          animation: fadeIn 1s ease-in;
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-bounce {
          animation: bounce 1s infinite;
        }
        .delay-150 {
          animation-delay: 0.15s;
        }
        .delay-300 {
          animation-delay: 0.3s;
        }
        @keyframes bounce {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-16px); }
        }
      `}</style>
    </>
  );
}
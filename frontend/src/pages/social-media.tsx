import type { NextPage } from 'next';
import Head from 'next/head';
import dynamic from 'next/dynamic';

const SocialMediaDashboard = dynamic(
  () => import('../components/SocialMediaDashboard/SocialMediaDashboard'),
  {
    ssr: false,
    loading: () => (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-500 via-purple-700 to-indigo-900">
        <div className="flex flex-col items-center space-y-6">
          <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-pink-400"></div>
          <p className="text-white text-xl font-semibold">Loading Social Media Dashboard...</p>
        </div>
      </div>
    ),
  }
);

const SocialMediaPage: NextPage = () => {
  const title = 'Social Media Analytics Dashboard';
  const description = 'Track and analyze your social media performance across all platforms';

  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="description" content={description} />
        <meta name="keywords" content="social media, analytics, dashboard, engagement, followers" />
      </Head>
      <div className="min-h-screen bg-gradient-to-br from-pink-500 via-purple-700 to-indigo-900 flex flex-col items-center justify-center px-4 py-10">
        <div className="mb-10 text-center">
          <h1 className="text-5xl md:text-6xl font-extrabold bg-gradient-to-r from-pink-400 via-purple-400 to-indigo-400 bg-clip-text text-transparent animate-gradient mb-4">
            {title}
          </h1>
          <p className="text-lg md:text-xl text-indigo-100">{description}</p>
        </div>
        <div className="w-full max-w-5xl bg-white/20 backdrop-blur-xl rounded-3xl shadow-2xl p-8 md:p-12 border border-white/30 mt-6">
          <SocialMediaDashboard />
        </div>
      </div>
      <style jsx global>{`
        @keyframes gradient {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }
        .animate-gradient {
          background-size: 200% 200%;
          animation: gradient 4s ease-in-out infinite;
        }
      `}</style>
    </>
  );
};

export default SocialMediaPage;
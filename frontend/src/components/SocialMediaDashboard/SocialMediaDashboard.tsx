import { useState, useEffect, FC } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Users, TrendingUp, Eye, MessageCircle, Share2, Heart, 
  Twitter, Instagram, Facebook, Linkedin, Zap, Calendar,
  RefreshCw, AlertCircle, BarChart3, PieChart, LineChart
} from 'lucide-react';
import { socialApiService, SocialStats, PlatformStats } from '../../services/socialApi';
import StatCard from './components/StatCard';
import PlatformCard from './components/PlatformCard';
import PostAnalytics from './components/PostAnalytics';
import AnalyticsCharts from './components/Charts/AnalyticsCharts';

interface PlatformData extends PlatformStats {
  icon: JSX.Element;
  color: string;
  gradient: string;
}

interface Post {
  id: number;
  title: string;
  engagement: number;
  likes: number;
  shares: number;
  platform: string;
  date: string;
  platformColor: string;
}

const MOCK_POSTS: Post[] = [
  { 
    id: 1, 
    title: 'Product Launch Announcement', 
    engagement: 2450, 
    likes: 1200, 
    shares: 85, 
    platform: 'Twitter',
    date: '2 hours ago',
    platformColor: 'border-blue-500'
  },
  { 
    id: 2, 
    title: 'Weekly Tips & Tricks', 
    engagement: 1870, 
    likes: 950, 
    shares: 42, 
    platform: 'Instagram',
    date: '5 hours ago',
    platformColor: 'border-pink-500'
  },
  { 
    id: 3, 
    title: 'Customer Success Story', 
    engagement: 3120, 
    likes: 1650, 
    shares: 120, 
    platform: 'Facebook',
    date: '1 day ago',
    platformColor: 'border-blue-600'
  },
];

// Animation variants
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.5,
      ease: "easeOut"
    }
  }
};

const SocialMediaDashboard: FC = () => {
  const [stats, setStats] = useState<SocialStats>({
    followers: 0,
    engagement: 0,
    reach: 0,
    impressions: 0,
    likes: 0,
    shares: 0,
  });

  const [platforms, setPlatforms] = useState<PlatformData[]>([]);
  const [posts, setPosts] = useState<Post[]>(MOCK_POSTS);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'overview' | 'analytics'>('overview');

  const platformConfigs = {
    twitter: { icon: <Twitter className="w-6 h-6" />, gradient: 'from-blue-500 to-cyan-500', color: 'bg-blue-500' },
    instagram: { icon: <Instagram className="w-6 h-6" />, gradient: 'from-pink-500 to-purple-500', color: 'bg-pink-500' },
    facebook: { icon: <Facebook className="w-6 h-6" />, gradient: 'from-blue-600 to-blue-800', color: 'bg-blue-600' },
    linkedin: { icon: <Linkedin className="w-6 h-6" />, gradient: 'from-blue-700 to-blue-900', color: 'bg-blue-700' },
  };

  const fetchSocialData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await socialApiService.getSocialStats();
      
      if (response.success) {
        setStats(response.data.totals);
        setLastUpdated(response.data.last_updated);
        
        const platformData: PlatformData[] = response.data.platforms.map(platform => ({
          ...platform,
          ...platformConfigs[platform.platform as keyof typeof platformConfigs]
        }));
        
        setPlatforms(platformData);
      } else {
        throw new Error('Failed to fetch data');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Error fetching social data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    await fetchSocialData();
  };

  useEffect(() => {
    fetchSocialData();
    const interval = setInterval(fetchSocialData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading && platforms.length === 0) {
    return (
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900 flex items-center justify-center"
      >
        <motion.div
          animate={{ 
            rotate: 360,
            scale: [1, 1.1, 1]
          }}
          transition={{ 
            rotate: { duration: 2, repeat: Infinity, ease: "linear" },
            scale: { duration: 1.5, repeat: Infinity }
          }}
          className="text-center"
        >
          <Zap className="w-16 h-16 text-cyan-400 mx-auto mb-4" />
          <p className="text-white text-xl">Initializing Dashboard...</p>
        </motion.div>
      </motion.div>
    );
  }

  return (
    <motion.main 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.8 }}
      className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900 text-white relative overflow-hidden"
    >
      {/* Enhanced Animated Background */}
      <div className="absolute inset-0">
        {/* Base Gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900" />
        
        {/* Animated Orbs */}
        <motion.div
          animate={{
            x: [0, 100, 0],
            y: [0, -50, 0],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"
        />
        
        <motion.div
          animate={{
            x: [0, -80, 0],
            y: [0, 60, 0],
          }}
          transition={{
            duration: 25,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 2
          }}
          className="absolute top-3/4 right-1/3 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl"
        />
        
        <motion.div
          animate={{
            x: [0, 120, 0],
            y: [0, 30, 0],
          }}
          transition={{
            duration: 30,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 1
          }}
          className="absolute bottom-1/4 left-1/3 w-64 h-64 bg-pink-500/10 rounded-full blur-3xl"
        />

        {/* Floating Particles */}
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            animate={{
              y: [0, -30, 0],
              opacity: [0.3, 0.8, 0.3],
            }}
            transition={{
              duration: 3 + Math.random() * 4,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
            className="absolute w-1 h-1 bg-white/30 rounded-full"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
          />
        ))}

        {/* Grid Pattern */}
        <div 
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: `linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)`,
            backgroundSize: '50px 50px',
          }}
        />
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <motion.header 
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <motion.div
            whileHover={{ scale: 1.05, rotate: 5 }}
            className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-2xl mb-6 shadow-2xl shadow-cyan-500/20"
          >
            <Zap className="w-10 h-10 text-white" />
          </motion.div>
          <motion.h1 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="text-5xl font-bold mb-4 bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent"
          >
            Social Media Analytics
          </motion.h1>
          <motion.p 
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.5 }}
            className="text-xl text-gray-300 max-w-2xl mx-auto leading-relaxed"
          >
            Real-time insights and performance metrics across all your social platforms
          </motion.p>
          
          {/* Navigation Tabs */}
          <motion.div 
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="flex justify-center space-x-4 mt-8"
          >
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setActiveTab('overview')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-2xl transition-all ${
                activeTab === 'overview' 
                  ? 'bg-white/20 shadow-lg backdrop-blur-sm' 
                  : 'bg-white/10 hover:bg-white/15 backdrop-blur-sm'
              }`}
            >
              <BarChart3 className="w-5 h-5" />
              <span>Overview</span>
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setActiveTab('analytics')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-2xl transition-all ${
                activeTab === 'analytics' 
                  ? 'bg-white/20 shadow-lg backdrop-blur-sm' 
                  : 'bg-white/10 hover:bg-white/15 backdrop-blur-sm'
              }`}
            >
              <LineChart className="w-5 h-5" />
              <span>Analytics</span>
            </motion.button>
          </motion.div>

          {/* Last Updated & Refresh */}
          <motion.div 
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="flex items-center justify-center space-x-4 mt-4"
          >
            {lastUpdated && (
              <span className="text-sm text-gray-400 bg-black/20 px-3 py-1 rounded-full backdrop-blur-sm">
                Last updated: {new Date(lastUpdated).toLocaleTimeString()}
              </span>
            )}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleRefresh}
              disabled={loading}
              className="flex items-center space-x-2 bg-white/10 hover:bg-white/20 px-4 py-2 rounded-lg transition-all disabled:opacity-50 backdrop-blur-sm border border-white/10"
            >
              <motion.div
                animate={{ rotate: loading ? 360 : 0 }}
                transition={{ duration: 1, repeat: loading ? Infinity : 0 }}
              >
                <RefreshCw className="w-4 h-4" />
              </motion.div>
              <span>{loading ? 'Refreshing...' : 'Refresh'}</span>
            </motion.button>
          </motion.div>
        </motion.header>

        {/* Error Message */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -20, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.9 }}
              className="bg-red-500/20 border border-red-500/50 rounded-2xl p-6 mb-8 flex items-center space-x-3 backdrop-blur-xl"
            >
              <AlertCircle className="w-6 h-6 text-red-400" />
              <div className="flex-1">
                <h3 className="font-semibold text-red-300">Error Loading Data</h3>
                <p className="text-red-200 text-sm">{error}</p>
              </div>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={fetchSocialData}
                className="bg-red-500/30 hover:bg-red-500/40 px-4 py-2 rounded-lg transition-colors backdrop-blur-sm"
              >
                Retry
              </motion.button>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Tab Content */}
        <AnimatePresence mode="wait">
          {activeTab === 'overview' ? (
            <motion.div
              key="overview"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3 }}
            >
              {/* Overall Stats Cards */}
              <motion.section 
                initial="hidden"
                animate="visible"
                className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6 mb-12"
              >
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.1 }}
                >
                  <motion.div
                    whileHover={{ scale: 1.08, boxShadow: '0 8px 32px rgba(0,255,255,0.15)' }}
                    whileTap={{ scale: 0.97 }}
                  >
                    <StatCard 
                      icon={<Users className="w-6 h-6" />} 
                      title="Total Followers" 
                      value={stats.followers} 
                      gradient="from-blue-500 to-cyan-500"
                      loading={loading}
                    />
                  </motion.div>
                </motion.div>
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                >
                  <motion.div
                    whileHover={{ scale: 1.08, boxShadow: '0 8px 32px rgba(0,255,127,0.15)' }}
                    whileTap={{ scale: 0.97 }}
                  >
                    <StatCard 
                      icon={<TrendingUp className="w-6 h-6" />} 
                      title="Engagement Rate" 
                      value={stats.engagement} 
                      suffix="%" 
                      gradient="from-green-500 to-emerald-500"
                      loading={loading}
                    />
                  </motion.div>
                </motion.div>
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.3 }}
                >
                  <motion.div
                    whileHover={{ scale: 1.08, boxShadow: '0 8px 32px rgba(255,0,255,0.15)' }}
                    whileTap={{ scale: 0.97 }}
                  >
                    <StatCard 
                      icon={<Eye className="w-6 h-6" />} 
                      title="Reach" 
                      value={stats.reach} 
                      gradient="from-purple-500 to-pink-500"
                      loading={loading}
                    />
                  </motion.div>
                </motion.div>
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.4 }}
                >
                  <motion.div
                    whileHover={{ scale: 1.08, boxShadow: '0 8px 32px rgba(255,127,0,0.15)' }}
                    whileTap={{ scale: 0.97 }}
                  >
                    <StatCard 
                      icon={<MessageCircle className="w-6 h-6" />} 
                      title="Impressions" 
                      value={stats.impressions} 
                      gradient="from-orange-500 to-red-500"
                      loading={loading}
                    />
                  </motion.div>
                </motion.div>
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.5 }}
                >
                  <motion.div
                    whileHover={{ scale: 1.08, boxShadow: '0 8px 32px rgba(255,0,127,0.15)' }}
                    whileTap={{ scale: 0.97 }}
                  >
                    <StatCard 
                      icon={<Heart className="w-6 h-6" />} 
                      title="Total Likes" 
                      value={stats.likes} 
                      gradient="from-pink-500 to-rose-500"
                      loading={loading}
                    />
                  </motion.div>
                </motion.div>
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.6 }}
                >
                  <motion.div
                    whileHover={{ scale: 1.08, boxShadow: '0 8px 32px rgba(127,0,255,0.15)' }}
                    whileTap={{ scale: 0.97 }}
                  >
                    <StatCard 
                      icon={<Share2 className="w-6 h-6" />} 
                      title="Shares" 
                      value={stats.shares} 
                      gradient="from-indigo-500 to-violet-500"
                      loading={loading}
                    />
                  </motion.div>
                </motion.div>
              </motion.section>

              {/* Platform Performance */}
              <motion.section
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="bg-white/5 backdrop-blur-xl rounded-3xl p-8 mb-8 border border-white/10 shadow-2xl"
              >
                <div className="flex items-center justify-between mb-8">
                  <h2 className="text-3xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                    🌐 Platform Performance
                  </h2>
                  <div className="flex items-center space-x-2 text-gray-400">
                    <Calendar className="w-5 h-5" />
                    <span>Live Data</span>
                  </div>
                </div>
                
                {platforms.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {platforms.map((platform, index) => (
                      <motion.div 
                        key={platform.platform}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.1 * index }}
                      >
                        <PlatformCard platform={platform} loading={loading} />
                      </motion.div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8 text-gray-400">
                    No platform data available
                  </div>
                )}
              </motion.section>

              {/* Top Performing Posts */}
              <motion.section
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="bg-white/5 backdrop-blur-xl rounded-3xl p-8 border border-white/10 shadow-2xl"
              >
                <h2 className="text-3xl font-bold mb-8 bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                  🔥 Top Performing Posts
                </h2>
                <div className="space-y-4">
                  {posts.map((post, index) => (
                    <motion.div 
                      key={post.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.5, delay: 0.1 * index }}
                      whileHover={{ scale: 1.03, boxShadow: '0 4px 24px rgba(255,255,255,0.10)' }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <PostAnalytics post={post} />
                    </motion.div>
                  ))}
                </div>
              </motion.section>
            </motion.div>
          ) : (
            <motion.div
              key="analytics"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              <AnalyticsCharts stats={stats} platforms={platforms} loading={loading} />
            </motion.div>
          )}
        </AnimatePresence>

        {/* API Status */}
        <motion.footer 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="text-center mt-12 text-gray-400"
        >
          <div className="flex items-center justify-center space-x-2 bg-black/20 px-4 py-2 rounded-full backdrop-blur-sm inline-flex">
            <motion.div
              animate={{ 
                scale: [1, 1.2, 1],
                opacity: [1, 0.7, 1]
              }}
              transition={{ 
                duration: 2, 
                repeat: Infinity 
              }}
              className={`w-2 h-2 rounded-full ${error ? 'bg-red-500' : 'bg-green-500'}`}
            />
            <span>{error ? 'API Connection Issues' : 'API Connected • Live Updates'}</span>
          </div>
        </motion.footer>
      </div>
    </motion.main>
  );
};

export default SocialMediaDashboard;
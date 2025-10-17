import dotenv from 'dotenv';
// Load environment variables at the very top
dotenv.config();

import compression from 'compression';
import cors from 'cors';
import express from 'express';
import helmet from 'helmet';
import morgan from 'morgan';
import authRoutes from '../src/routes/authRoutes';
import { Middleware_404 } from './middleware/404HandlingMiddleware';
import { errorMiddleware } from './middleware/errorHandlingMiddleware';
import { limiter } from './middleware/rateLimiterMiddleware';
import contributorsRouter from "./routes/contributors.routes";
import healthRouter from "./routes/health.routes";
import projectRouter from "./routes/projects.routes";
import statsRouter from "./routes/stats.routes";


const app = express();
const PORT = process.env.PORT || 3001;

// Core Middleware
app.use(helmet());
app.use(cors());
app.use(compression());
app.use(morgan('combined'));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Apply rate limiting to all incoming requests
app.use(limiter);

// --- Application Routes ---
app.use(healthRouter);
app.use('/api/auth', authRoutes); // All auth routes are prefixed with /api/auth
app.use(statsRouter);
app.use(contributorsRouter);
app.use(projectRouter);

// --- Error Handling ---

// Custom error handling middleware should be after all routes
app.use(errorMiddleware);

// The 404 handler must be the LAST middleware to catch all unhandled requests
app.use(Middleware_404);

// Passport.js setup
if (process.env.USE_OAUTH === 'true') {
  require('../config/passport-setup');
  const oAuthRoutes = require('./routes/oAuthRoutes')

  app.use('/api/auth', oAuthRoutes);
}

app.listen(PORT, () => {
  console.log(`🎃 Hacktoberfest 2025 API running on port ${PORT}`);
  console.log(`🌍 Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`🚀 Health check: http://localhost:${PORT}/health`);
  console.log(`🔐 Auth routes: http://localhost:${PORT}/api/auth`);
});
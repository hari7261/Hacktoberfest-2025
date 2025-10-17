import express from 'express';
import passport from 'passport';
import { githubCallback } from '../oauth/strategies/githubStrategy';
import { googleCallback } from '../oauth/strategies/googleStrategy';

const router = express.Router();

// Google
router.get("/oauth/google", passport.authenticate('google', { scope: ['profile', 'email'] }));
router.get("/oauth/google/callback", passport.authenticate('google', {session: false}), googleCallback);
// Github
router.get("/oauth/github", passport.authenticate('github', { scope: ['user:email'] }));
router.get("/oauth/github/callback", passport.authenticate('github', {session: false}), githubCallback);

export default router;
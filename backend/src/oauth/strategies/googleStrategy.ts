
import { Strategy as GoogleStrategy, Profile, VerifyCallback } from 'passport-google-oauth20';
import process from 'process';
import { users } from "../../controllers/authController";
import { generateToken } from '../../utils/auth';

const clientID: string = process.env.GOOGLE_CLIENT_ID || '';
const clientSecret: string = process.env.GOOGLE_CLIENT_SECRET || '';

export const GoogleOauth = new GoogleStrategy({
    clientID: clientID,
    clientSecret: clientSecret,
    callbackURL: '/api/auth/oauth/google/callback'
  }, (accessToken: string, refreshToken: string, profile: Profile, cb: VerifyCallback) => {
    if (!profile.emails || profile.emails.length === 0) {
      return cb(new Error('No emails associated with this account!'), false);
    }
    
    const email = profile.emails[0].value;
    const user = users.find(u => email === u.email);
        
    if (!user) {
      const newUser = {
        id: profile.id,
        email: email,
        password: null,
        name: profile.displayName,
        createdAt: new Date()
      };
      users.push(newUser);

      return cb(null, newUser);
    }

    return cb(null, user);
});

export const googleCallback = (req: any, res: any) => {
  const user = req.user;

  if (!user) {
    res.status(400).json({ 
        success: false,
        message: 'Authentication failed' 
      });
    return;
  }

  const token = generateToken(user.id, user.email);

  res.json({
    success: true,
    message: 'Login successful',
    token,
    user: {
      id: user.id,
      email: user.email,
      name: user.name
    }
  });
}
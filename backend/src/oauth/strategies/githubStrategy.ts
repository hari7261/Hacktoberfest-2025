import { Strategy as GithubStrategy, Profile } from 'passport-github2';
import { users } from '../../controllers/authController';
import { generateToken } from '../../utils/auth';

const clientID: string = process.env.GITHUB_CLIENT_ID || '';
const clientSecret: string = process.env.GITHUB_CLIENT_SECRET || '';

export const GithubOauth = new GithubStrategy({
    clientID: clientID,
    clientSecret: clientSecret,
    callbackURL: '/api/auth/oauth/github/callback'
    }, async (accessToken: string, refreshToken: string, profile: Profile, cb: any) => {
        let githubMail = null;

        if (!profile.emails || profile.emails.length === 0) {
            githubMail = await fetchEmailWithGithubApi(accessToken);

            if (!githubMail) {
                return cb(new Error('No emails associated with this account!'), false);
            }

        }
            
        const email = profile.emails ? profile.emails[0].value : githubMail;
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

export const githubCallback = (req: any, res: any) => {
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

const fetchEmailWithGithubApi = async (accessToken: string) => {
    const emailResponse = await fetch('https://api.github.com/user/emails', {
        headers: {
            'Accept': 'application/vnd.github+json',
            'Authorization': `BEARER ${accessToken}`
        }
    });

    const emails = await emailResponse.json();
    const primaryEmailObj = emails.find((email: { primary: boolean; verified: boolean; }) => email.primary === true && email.verified === true);
    
    return primaryEmailObj ? primaryEmailObj.email : null;
}
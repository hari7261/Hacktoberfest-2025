import passport from "passport";
import { GithubOauth } from "../src/oauth/strategies/githubStrategy";
import { GoogleOauth } from "../src/oauth/strategies/googleStrategy";

passport.initialize();
passport.session();

passport.use(GoogleOauth);
passport.use(GithubOauth);
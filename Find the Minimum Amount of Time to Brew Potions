class Solution {
    public long minTime(int[] skill, int[] mana) {
        int n = skill.length;
        int m = mana.length;

        long[] f = new long[n];
        
        for (int j = 0; j < m; j++) {
            long x = mana[j];
            long current = f[0]; 
            
            for (int i = 1; i < n; i++) {
                current = Math.max(current + (long) skill[i - 1] * x, f[i]);
            }
            
            f[n - 1] = current + (long) skill[n - 1] * x;
            
            for (int i = n - 2; i >= 0; i--) {
                f[i] = f[i + 1] - (long) skill[i + 1] * x;
            }
        }
        
        return f[n - 1];
    }
}

import 'dart:math';

// Original implementation
bool isPrime(int n) {
  if (n <= 1) return false;
  if (n <= 3) return true;
  if (n % 2 == 0 || n % 3 == 0) return false;
  int i = 5;
  while (i * i <= n) {
    if (n % i == 0 || n % (i + 2) == 0) return false;
    i += 6;
  }
  return true;
}

/// Modular exponentiation: (base^exp) mod mod
int modPow(int base, int exp, int mod) {
  int result = 1;
  base = base % mod;
  while (exp > 0) {
    if (exp % 2 == 1) {
      result = (result * base) % mod;
    }
    exp = exp ~/ 2;
    base = (base * base) % mod;
  }
  return result;
}

/// Miller-Rabin primality test implementation
bool isPrimeMillerRabin(int n, [int k = 10]) {
  if (n <= 1) return false;
  if (n <= 3) return true;
  if (n % 2 == 0) return false;

  // Write n-1 as d * 2^r
  int d = n - 1;
  int r = 0;
  while (d % 2 == 0) {
    d ~/= 2;
    r++;
  }

  // Perform k rounds of testing
  Random random = Random();
  for (int i = 0; i < k; i++) {
    int a = 2 + random.nextInt(n - 3);
    int x = modPow(a, d, n);
    
    if (x == 1 || x == n - 1) continue;
    
    bool composite = true;
    for (int j = 0; j < r - 1; j++) {
      x = modPow(x, 2, n);
      if (x == n - 1) {
        composite = false;
        break;
      }
    }
    
    if (composite) return false;
  }
  
  return true;
}

/// Performance benchmark comparing algorithms
void benchmarkPrimalityTests() {
  List<int> testNumbers = [
    97, 982451653, 1000000007, 1000000009,
    2147483647, 15485863, 32452843, 49979687
  ];
  
  print('Performance Benchmark: Original vs Miller-Rabin\n');
  print('Number\t\tOriginal (μs)\tMiller-Rabin (μs)\tSpeedup');
  print('-' * 65);
  
  for (int n in testNumbers) {
    // Benchmark original algorithm
    Stopwatch sw = Stopwatch()..start();
    bool originalResult = isPrime(n);
    sw.stop();
    int originalTime = sw.elapsedMicroseconds;
    
    // Benchmark Miller-Rabin
    sw.reset();
    sw.start();
    bool millerRabinResult = isPrimeMillerRabin(n);
    sw.stop();
    int millerRabinTime = sw.elapsedMicroseconds;
    
    double speedup = originalTime / millerRabinTime;
    String consistent = originalResult == millerRabinResult ? '✓' : '✗';
    
    print('$n\t${originalTime}\t\t${millerRabinTime}\t\t\t${speedup.toStringAsFixed(2)}x $consistent');
  }
}

List<int> primeFactors(int n) {
  List<int> factors = [];
  var num = n;
  // count number of 2s
  while (num % 2 == 0) {
    factors.add(2);
    num ~/= 2;
  }
  // odd factors
  for (int i = 3; i * i <= num; i += 2) {
    while (num % i == 0) {
      factors.add(i);
      num ~/= i;
    }
  }
  // if remaining > 2 it's prime
  if (num > 2) {
    factors.add(num);
  }
  return factors;
}

void main(List<String> args) {
  if (args.isEmpty) {
    print('Usage: dart primechecker.dart <number> [benchmark]');
    print('  <number>   - Check if number is prime');
    print('  benchmark  - Run performance comparison');
    return;
  }
  
  if (args[0] == 'benchmark') {
    benchmarkPrimalityTests();
    return;
  }
  
  final n = int.tryParse(args[0]);
  if (n == null) {
    print('Please pass a valid integer.');
    return;
  }

  print('Is $n prime? ${isPrime(n)}');
  print('Prime factors of $n: ${primeFactors(n)}');
  
  // Show comparison between algorithms
  print('\nAlgorithm Comparison:');
  
  Stopwatch sw = Stopwatch();
  
  sw.start();
  bool originalResult = isPrime(n);
  sw.stop();
  int originalTime = sw.elapsedMicroseconds;
  
  sw.reset();
  sw.start();
  bool millerRabinResult = isPrimeMillerRabin(n);
  sw.stop();
  int millerRabinTime = sw.elapsedMicroseconds;
  
  print('Original algorithm: $originalResult (${originalTime}μs)');
  print('Miller-Rabin: $millerRabinResult (${millerRabinTime}μs)');
  
  if (originalTime > 0 && millerRabinTime > 0) {
    double speedup = originalTime / millerRabinTime;
    print('Miller-Rabin is ${speedup.toStringAsFixed(2)}x faster');
  }
}
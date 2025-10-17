import java.util.Scanner;

public class ignoreFiveSum {
	public static void main(String[] args) {
		int sum = 0, n ;
		Scanner sc = new Scanner(System.in);
		for (int i = 0; i < 10; i++) {
			n = sc.nextInt();
			if (n % 5 == 0 && n % 10 != 0) {
				sum = sum + 0;
			} else {
				sum = sum + n;
			}
			System.out.print("Sum : ");
			System.out.println(sum);
			sc.close();
		}
	}
}
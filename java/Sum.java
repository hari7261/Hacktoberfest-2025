import java.util.Scanner;

public class Sum {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		System.out.print("Enter three numbers : ");
		int a = scan.nextInt();
		int b = scan.nextInt();
		int c = scan.nextInt();
		int d = a+b+c;
		System.out.println("Sum of three numbers is :  "+d);
		scan.close();
	}
}
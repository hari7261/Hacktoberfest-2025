import java.util.Scanner;

public class kmtomiles {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		System.out.print("Enter the length in km: ");
		double km = scan.nextDouble();
		double miles = km / 0.6214;
		System.out.println("The length in miles is : " + miles);
		scan.close();
	}
}
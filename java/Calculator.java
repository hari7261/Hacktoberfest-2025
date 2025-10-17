import java.util.*;


class SwitchCase {

	int a, b, choice, d;
	void input() {
		Scanner scan = new Scanner(System.in);
		System.out.println("1 : Addition\n2 : Subtraction\n3 : Multiplication\n4 : Division\nEnter choice");
		choice = scan.nextInt();
		System.out.println("Enter the value of a: ");
		a = scan.nextInt();
		System.out.println("Enter the value of b: ");
		b = scan.nextInt();
		// sc.close();

	}

	void Calculate() {

		input();
		switch (choice) {
		case 1:
			d = a + b;
			System.out.println("Result: " + d);
			break;

		case 2:
			d = a - b;
			System.out.println("Result: " + d);
			break;

		case 3:
			d = a * b;
			System.out.println("Result: " + d);
			break;

		case 4:
			try {
				d = a / b;
				System.out.println("Result: " + d);
				break;
			} catch (ArithmeticException e) {
				System.out.println("Division not possible");
				System.out.println(e.getMessage());
				break;
			}
		default:
			System.out.println("Invalid Choice Input");
			break;
		}

	}
}

public class Calculator {

	public static void main(String[] args) {
		SwitchCase sw = new SwitchCase();
		Scanner scan = new Scanner(System.in);
		boolean ag;
		do {
			sw.Calculate();
			System.out.println("Do you want to perform another calculation? (y/n): ");
			char again = scan.next().charAt(0);

			if (again == 'y' || again == 'Y') {
				ag = true;
			} else if (again == 'n' || again == 'N') {
				ag = false;
			}
			else {
				System.out.println("Invalid Input. Exiting.");
				ag = false;
			}
		} while(ag);
		scan.close();
		
	}
}

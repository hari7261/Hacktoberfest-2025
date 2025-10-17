import java.util.*;

public class Flames {
	public void getInput() {
		Scanner sc = new Scanner(System.in);

		String str1 = sc.next().toLowerCase();
		String str2 = sc.next().toLowerCase();

		commonLetter(str1, str2);
		sc.close();

	}

	public int commonLetter(String str1, String str2) {
		int count = 0;
		char[] str1Array = str1.toCharArray();
		char[] str2Array = str2.toCharArray();

		for (int i : str1Array) {
			for (int j : str2Array) {
				if (i == j) {
					count++;
				}
			}

		}
		return count;
	}

	public static void main(String[] args) {
		Flames f = new Flames();
		f.getInput();

	}
}
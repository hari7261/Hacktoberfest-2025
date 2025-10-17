import java.util.Scanner;

public class stringMethods {

    // static String Original = "Welcome To Java";

    int strlen(String str) {
        int len = str.length();
        // System.out.println("The length of the string is: " + len);
        return len;

    }

    String strrev(String str) {
        String forwardStr = str;
        String reversedStr = "";

        for (int i = 0; i < forwardStr.length(); i++) {
            reversedStr = forwardStr.charAt(i) + reversedStr;
        }
        return reversedStr;
    }
    
    String strappend(String Original,String str) {
        
        return (Original + " " + str);
    }

    String strcon(String str1, String str2) {

        return (str1.concat(str2));
    }
    
    public static void main(String[] args) {
        
        Scanner scan = new Scanner(System.in);
        stringMethods str = new stringMethods();
        
        System.out.println("Enter a string: ");
        String Original = scan.nextLine();
        
        int str_len = str.strlen(Original); // Length of the string
        System.out.println("The length of the string is: " + str_len);
        
        String reversed = str.strrev(Original); // Reverse the string
        System.out.println("The reversed string is: " + reversed);


        System.out.println("Enter a string to append: ");
        String app = scan.nextLine();
        String app_str = str.strappend(Original,app); // string append
        System.out.println("After appending: " + app_str);

        System.out.println("Enter a string to concatenate: ");
        String con = scan.nextLine();

        String concat = str.strcon(Original, con); // string concatination
        System.out.println("After concatenating: " + concat);

        scan.close();
    }
}